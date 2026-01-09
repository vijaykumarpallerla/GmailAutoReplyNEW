import os
import logging
import threading
import time
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

_scheduler = None
_loop_thread = None
_loop_stop = False
_busy_lock = threading.Lock()

# In-memory failure tracking (user_id -> consecutive failure count)
_fail_counts = {}
# In-memory pause timestamps (user_id -> unix timestamp until which we skip)
_pause_until = {}

# Global configuration for pull interval
INTERVAL_SECONDS = 28

# Default behavior: threshold and cooldown (seconds)
FAIL_THRESHOLD = int(getattr(__import__('django.conf').conf.settings, 'SCHEDULER_FAIL_THRESHOLD', 2))
FAIL_COOLDOWN_SECONDS = int(getattr(__import__('django.conf').conf.settings, 'SCHEDULER_FAIL_COOLDOWN_SECONDS', 60))
# How long to show auth-issue notice in UI (seconds) when an auth error occurs
AUTH_ISSUE_UI_SECONDS = int(getattr(__import__('django.conf').conf.settings, 'SCHEDULER_AUTH_ISSUE_UI_SECONDS', 86400))

def _should_start_scheduler() -> bool:
    """Ensure we only start once in the Django autoreload 'main' process."""
    # Allow explicit opt-out in any environment
    if os.environ.get("DISABLE_IN_APP_SCHEDULER") == "1":
        return False
    # When runserver uses the auto-reloader, Django sets RUN_MAIN='true' in the child.
    run_main = os.environ.get("RUN_MAIN") == "true"
    # If not using runserver (e.g., gunicorn) there might be no RUN_MAIN; allow start in DEBUG.
    if settings.DEBUG:
        return run_main or os.environ.get("RUN_MAIN") is None
    # In non-DEBUG, only start if explicitly enabled via env.
    return os.environ.get("ENABLE_IN_APP_SCHEDULER") == "1"


def start_scheduler():
    global _scheduler
    if _scheduler is not None:
        return
    if not _should_start_scheduler():
        return

    # Try APScheduler first
    try:
        from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
        from apscheduler.executors.pool import ThreadPoolExecutor  # type: ignore
        from apscheduler.jobstores.memory import MemoryJobStore  # type: ignore

        # max_workers=150: Future-proof for up to 150 users
        # Only active threads = number of actual users (e.g., 50 users = 50 threads)
        # Unused capacity doesn't consume resources
        executors = {"default": ThreadPoolExecutor(max_workers=150)}
        jobstores = {"default": MemoryJobStore()}

        scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, timezone=str(getattr(settings, "TIME_ZONE", "UTC")))
        scheduler.add_job(
            func=_pull_for_all_connected_users,
            trigger="interval",
            seconds=INTERVAL_SECONDS,
            id="gmail_pull_all_users",
            replace_existing=True,
            coalesce=True,
            max_instances=10,
        )
        # Cleanup old ReplyLog entries every 24 hours (runs at midnight UTC)
        scheduler.add_job(
            func=_cleanup_old_replies,
            trigger="interval",
            hours=24,
            id="cleanup_old_replies",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
        )
        scheduler.start()
        _scheduler = scheduler
        logger.info("Started in-app Gmail pull scheduler (APScheduler) every %ss", INTERVAL_SECONDS)
        return
    except Exception as exc:
        logger.warning("APScheduler not available, falling back to simple loop: %s", exc)

    # Fallback: simple background thread loop
    def _loop():
        global _loop_stop
        logger.info("Started in-app Gmail pull simple loop every %ss", INTERVAL_SECONDS)
        while not _loop_stop:
            started = time.time()
            acquired = _busy_lock.acquire(blocking=False)
            if acquired:
                try:
                    _pull_for_all_connected_users()
                except Exception:
                    logger.exception("Auto-pull loop error")
                finally:
                    _busy_lock.release()
            else:
                logger.debug("Previous auto-pull still running, skipping tick")
            elapsed = time.time() - started
            # Sleep remaining interval (avoid thrashing)
            delay = max(1.0, INTERVAL_SECONDS - elapsed)
            time.sleep(delay)

    t = threading.Thread(target=_loop, name="gmail-auto-pull", daemon=True)
    t.start()
    globals()["_loop_thread"] = t


def _pull_for_all_connected_users():
    from .models import GmailToken
    from .gmail_service import gmail_pull_for_user
    import concurrent.futures
    from django.core.cache import cache

    User = get_user_model()
    tokens = list(GmailToken.objects.select_related("user").all())
    
    if not tokens:
        return

    processed_total = 0
    matched_total = 0
    sent_total = 0
    skipped_total = 0

    # Helper function for the thread
    def process_one_user(token):
        try:
            ts = datetime.now().strftime('%H:%M:%S')
            # Changed to debug to reduce console noise as per user request
            logger.debug(f"[{ts}] Pulling requests for user {token.user.username}")
            # Skip if user is currently paused due to recent failures
            uid = int(token.user.pk)
            now_ts = datetime.now().timestamp()
            until = _pause_until.get(uid)
            if until and now_ts < until:
                logger.info(f"Skipping user {token.user.username} until {datetime.fromtimestamp(until)} due to recent failures")
                return {'error': 'paused'}

            # q="" is fine now as gmail_service handles the default fallback logic internally
            result = gmail_pull_for_user(user=token.user, max_results=20)

            # Handle structured errors returned by gmail_service
            if isinstance(result, dict) and result.get('error') == 'network':
                # increment fail count
                _fail_counts[uid] = _fail_counts.get(uid, 0) + 1
                logger.warning("Network error for user %s (count=%s)", token.user.username, _fail_counts[uid])
                if _fail_counts[uid] >= FAIL_THRESHOLD:
                    _pause_until[uid] = now_ts + FAIL_COOLDOWN_SECONDS
                    logger.info("Pausing pulls for user %s for %ss after %s failures", token.user.username, FAIL_COOLDOWN_SECONDS, _fail_counts[uid])
                return result
            elif isinstance(result, dict) and result.get('error') == 'auth':
                # Mark auth issue in cache so UI can show "Please logout and login"
                cache_key = f"gmail_auth_issue_{token.user.pk}"
                try:
                    cache.set(cache_key, True, AUTH_ISSUE_UI_SECONDS)
                except Exception:
                    # Cache may not be configured; swallow error but log
                    logger.exception("Failed to set auth issue cache for user %s", token.user.pk)
                # reset fail count but do not pause long-term (user requested no auth pause)
                _fail_counts.pop(uid, None)
                _pause_until.pop(uid, None)
                logger.warning("Auth issue for user %s: UI will show re-login prompt", token.user.username)
                return result
            else:
                # success: reset any failure counter/pause
                _fail_counts.pop(uid, None)
                _pause_until.pop(uid, None)
                # Also clear any auth cache flag if present
                try:
                    cache.delete(f"gmail_auth_issue_{token.user.pk}")
                except Exception:
                    pass
                return result
        except Exception as exc:
            # For 404 errors (deleted messages), just log without traceback
            exc_str = str(exc)
            if '404' in exc_str or 'not found' in exc_str.lower():
                logger.warning("Gmail auto-pull: Message not found (404) for user %s", token.user.pk)
            else:
                logger.exception("Gmail auto-pull failed for user %s: %s", token.user.pk, exc)
            return {}

    # Use ThreadPoolExecutor to run in parallel
    # Reduced max_workers to 20 to avoid too many simultaneous outbound connections
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_user = {executor.submit(process_one_user, t): t.user for t in tokens}
        
        for future in concurrent.futures.as_completed(future_to_user):
            try:
                # Add timeout so one slow user doesn't block the next 28s cycle for everyone
                result = future.result(timeout=40)
                processed_total += result.get("processed", 0)
                matched_total += result.get("matched", 0)
                sent_total += result.get("sent", 0)
                skipped_total += result.get("skipped", 0)
            except concurrent.futures.TimeoutError:
                u = future_to_user[future]
                logger.error(f"Timed out waiting for user {u.username}")
            except Exception as e:
                logger.error(f"Worker exception: {e}")

    # Calculate next expected pull time
    next_pull_time = datetime.now() + timedelta(seconds=INTERVAL_SECONDS)
    next_pull_str = next_pull_time.strftime('%H:%M:%S')

    logger.debug(
        "Gmail auto-pull run done (Parallel) processed=%s matched=%s sent=%s skipped=%s",
        processed_total,
        matched_total,
        sent_total,
        skipped_total,
    )
    # Log the next expected pull time clearly for debugging
    logger.info(f"Cycle Complete. Next pull expected at: {next_pull_str}")


def _cleanup_old_replies():
    """
    Cleanup job: Delete ReplyLog entries older than 150 days.
    Runs automatically every 24 hours via APScheduler.
    """
    from .gmail_service import cleanup_old_reply_logs
    
    try:
        deleted_count = cleanup_old_reply_logs(days_to_keep=150)
        if deleted_count > 0:
            logger.info("Cleanup: Deleted %d old ReplyLog entries", deleted_count)
    except Exception as exc:
        logger.exception("Cleanup job failed: %s", exc)