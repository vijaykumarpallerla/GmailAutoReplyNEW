from django.apps import AppConfig


class AutoReplyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auto_reply'

    def ready(self):
        # Start in-app scheduler (non-blocking). Safe if APScheduler missing.
        try:
            from . import scheduler
            scheduler.start_scheduler()
        except Exception:
            # Avoid raising during app registry; log silently.
            import logging
            logging.getLogger(__name__).debug("Scheduler start skipped", exc_info=True)
