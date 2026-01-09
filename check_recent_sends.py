import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule, User, ReplyLog
from datetime import datetime, timedelta

# Get the most recent email sent by Neelam for rule 64
user = User.objects.get(username='neelam')
rule = AutoReplyRule.objects.get(id=64, user=user)

# Check recent reply logs for this rule
recent_logs = ReplyLog.objects.filter(
    user=user,
    rule=rule
).order_by('-sent_at')[:5]

print("=" * 80)
print(f"Recent reply logs for Neelam's rule 64 (Guidewire Developers)")
print("=" * 80)

if not recent_logs:
    print("\n✗ No recent reply logs found")
    print("\nTo test all 3 attachments, we need an actual email send.")
    print("Checking if there are any emails matching this rule...")
    
    # Let's check what triggers this rule
    from auto_reply.models import RuleCondition
    conditions = RuleCondition.objects.filter(rule=rule)
    print(f"\nRule conditions:")
    for cond in conditions:
        print(f"  {cond.condition_type}: {cond.condition_value}")
    
else:
    for log in recent_logs:
        print(f"\nDate: {log.sent_at}")
        print(f"  Rule: {log.rule.rule_name}")
        print(f"  From: {log.inbound_id}")
        print(f"  Subject: {log.subject[:60]}...")
        print(f"  Sent: {log.sent}")
