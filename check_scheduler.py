import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply import scheduler

print("\n" + "="*80)
print("SCHEDULER STATUS")
print("="*80)

if scheduler._scheduler is not None:
    print("✅ APScheduler is RUNNING")
    jobs = scheduler._scheduler.get_jobs()
    print(f"\nScheduled jobs: {len(jobs)}")
    for job in jobs:
        print(f"  - {job.id}: next run at {job.next_run_time}")
elif scheduler._loop_thread is not None:
    print("✅ Simple loop scheduler is RUNNING")
    print(f"  Thread alive: {scheduler._loop_thread.is_alive()}")
else:
    print("❌ NO SCHEDULER IS RUNNING")
    print("\nReasons:")
    print(f"  - DEBUG mode: {django.conf.settings.DEBUG}")
    print(f"  - RUN_MAIN env: {os.environ.get('RUN_MAIN')}")
    print(f"  - DISABLE_IN_APP_SCHEDULER: {os.environ.get('DISABLE_IN_APP_SCHEDULER')}")
    print(f"  - ENABLE_IN_APP_SCHEDULER: {os.environ.get('ENABLE_IN_APP_SCHEDULER')}")
    print("\n  To enable scheduler:")
    print("    Set environment variable: ENABLE_IN_APP_SCHEDULER=1")
    print("    Or restart server to trigger RUN_MAIN=true")

print("="*80)
