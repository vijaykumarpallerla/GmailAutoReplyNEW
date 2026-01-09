import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule, User, ReplyLog
import json

# Get the most recent email sent by Neelam for rule 64
user = User.objects.get(username='neelam')
rule = AutoReplyRule.objects.get(id=64, user=user)

# Check the most recent reply log
recent_log = ReplyLog.objects.filter(
    user=user,
    rule=rule
).order_by('-sent_at').first()

print("=" * 80)
print(f"Most Recent Send for Neelam's rule 64")
print("=" * 80)

if recent_log:
    print(f"\nSent at: {recent_log.sent_at}")
    print(f"To: {recent_log.to_email}")
    print(f"Subject: {recent_log.subject}")
    print(f"Inbound ID: {recent_log.inbound_id}")
    print(f"\nMeta data:")
    if recent_log.meta:
        print(json.dumps(recent_log.meta, indent=2))
    else:
        print("  (empty)")
else:
    print("✗ No recent sends found for this rule")
    
    # Check if there are any reply logs at all for Neelam
    all_logs = ReplyLog.objects.filter(user=user).order_by('-sent_at')[:3]
    if all_logs:
        print(f"\nBut found {len(all_logs)} other recent sends:")
        for log in all_logs:
            print(f"  {log.sent_at} - {log.rule.rule_name if log.rule else 'No rule'} to {log.to_email}")
