import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.models import ReplyLog, AutoReplyRule
from django.utils import timezone
from datetime import timedelta

print("\n" + "="*80)
print("RECENT EMAIL AUTO-REPLIES (Last 30 minutes)")
print("="*80)

# Get recent replies
recent_time = timezone.now() - timedelta(minutes=30)
recent_replies = ReplyLog.objects.filter(sent_at__gte=recent_time).order_by('-sent_at')

print(f"\nTotal replies sent: {recent_replies.count()}")
print("\nDetails:")
print("-"*80)

if recent_replies.count() == 0:
    print("❌ No auto-replies sent in the last 30 minutes")
    print("\nPossible reasons:")
    print("  1. No incoming emails matched any active rules")
    print("  2. Gmail pull hasn't run yet (check if scheduler is running)")
    print("  3. Rules might be disabled")
else:
    for i, reply in enumerate(recent_replies[:10], 1):
        print(f"\n{i}. Reply sent at: {reply.sent_at}")
        print(f"   To: {reply.to_email}")
        print(f"   Subject: {reply.subject[:50] if reply.subject else 'N/A'}...")
        print(f"   Rule ID: {reply.rule.id if reply.rule else 'N/A'}")
        print(f"   Thread ID: {reply.thread_id[:20] if reply.thread_id else 'N/A'}...")
        meta = reply.meta or {}
        print(f"   Success: {'✅ YES' if meta.get('success', True) else '❌ NO'}")
        print(f"   Attachments: {len(meta.get('attachments_sent', []))}")
        if meta.get('error_message'):
            print(f"   Error: {meta['error_message']}")

print("\n" + "="*80)
print("ACTIVE RULES")
print("="*80)

active_rules = AutoReplyRule.objects.filter(is_active=True)
print(f"\nTotal active rules: {active_rules.count()}")

for rule in active_rules:
    actions = rule.actions.all()
    print(f"\n  Rule #{rule.id}: {rule.name}")
    print(f"    User: {rule.user.username}")
    print(f"    Conditions: {rule.conditions.count()}")
    print(f"    Actions: {actions.count()}")
    for action in actions:
        att_count = len(action.attachments or [])
        print(f"      - {action.action_type}: {att_count} attachments")

print("\n" + "="*80)
