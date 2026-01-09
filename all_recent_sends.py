import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule, User, ReplyLog
import json

# Get all sends for rule 64 in the last hour
user = User.objects.get(username='neelam')
rule = AutoReplyRule.objects.get(id=64, user=user)

recent_logs = ReplyLog.objects.filter(
    user=user,
    rule=rule
).order_by('-sent_at')[:10]

print("=" * 80)
print(f"All recent sends for Neelam's rule 64 (last 10)")
print("=" * 80)

for i, log in enumerate(recent_logs, 1):
    print(f"\n{i}. Sent at: {log.sent_at}")
    print(f"   Subject: {log.subject[:50]}")
    print(f"   To: {log.to_email}")
    if log.meta and 'attachments' in log.meta:
        attachments = log.meta.get('attachments')
        print(f"   Attachments: {attachments}")
    print(f"   Inbound ID: {log.inbound_id}")
