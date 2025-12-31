import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.models import ReplyLog
from django.db.models import Count

print("\n" + "="*70)
print("DUPLICATE CHECK - DATABASE VERIFICATION")
print("="*70)

# Check for duplicates: same user + thread_id + rule
dups = ReplyLog.objects.values('user', 'thread_id', 'rule').annotate(count=Count('id')).filter(count__gt=1)

print(f"\nSearching for duplicates (same user + thread + rule)...")
print(f"Found: {dups.count()} duplicates\n")

if dups.count() > 0:
    print("DUPLICATES FOUND:")
    for d in dups:
        print(f"  User {d['user']}, Thread {d['thread_id']}, Rule {d['rule']}: {d['count']} entries")
else:
    print("✅ NO DUPLICATES - PERFECT DEDUPLICATION!")

print(f"\nTotal ReplyLog entries: {ReplyLog.objects.count()}")

# Show recent threads with reply counts
print("\n" + "="*70)
print("RECENT THREADS - REPLY COUNTS")
print("="*70)

from django.contrib.auth.models import User
for user in User.objects.all():
    logs = ReplyLog.objects.filter(user=user).order_by('-sent_at')[:10]
    if logs:
        print(f"\n{user.username} (last 10 threads):")
        thread_counts = {}
        for log in logs:
            tid = log.thread_id
            if tid not in thread_counts:
                thread_counts[tid] = 0
            thread_counts[tid] += 1
        
        for tid, count in thread_counts.items():
            status = "✅ OK" if count == 1 else f"⚠️ {count} REPLIES"
            print(f"  Thread {tid}: {count} reply(s) {status}")
