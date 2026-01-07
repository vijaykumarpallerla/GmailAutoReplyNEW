"""Check most recent email log for vijayypallerla"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

u = User.objects.get(email='vijayypallerla@gmail.com')
log = ReplyLog.objects.filter(user=u).order_by('-sent_at').first()

print("\n" + "="*100)
print("MOST RECENT EMAIL SENT by vijayypallerla")
print("="*100 + "\n")

if log:
    attachments = log.meta.get('attachments', 0) if log.meta else 0
    print(f"To: {log.to_email}")
    print(f"Time: {log.sent_at}")
    print(f"Subject: {log.subject}")
    print(f"Attachments: {attachments}")
    print(f"Rule: {log.rule.rule_name if log.rule else 'N/A'}")
    print(f"Thread ID: {log.thread_id}")
    print(f"Message ID: {log.message_id}")
else:
    print("No logs found")

print("\n" + "="*100 + "\n")
