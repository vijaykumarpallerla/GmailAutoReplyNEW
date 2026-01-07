"""List last 10 emails for user 'are' with attachment counts"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

u = User.objects.get(username='are')
logs = ReplyLog.objects.filter(user=u).order_by('-sent_at')[:10]

print(f"Last 10 emails for {u.username}\n" + "="*80)
for i, log in enumerate(logs, 1):
    attachments = log.meta.get('attachments', 0) if log.meta else 0
    print(f"{i}. To: {log.to_email}")
    print(f"   Time: {log.sent_at}")
    print(f"   Attachments: {attachments}")
    print(f"   Rule: {log.rule.rule_name if log.rule else 'N/A'}")
    print(f"   Subject: {log.subject}")
    print()
