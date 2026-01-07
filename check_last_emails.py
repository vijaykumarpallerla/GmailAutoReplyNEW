"""Check last 10 emails sent by vijayypallerla"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

u = User.objects.get(email='vijayypallerla@gmail.com')
logs = ReplyLog.objects.filter(user=u).order_by('-sent_at')[:10]

print(f"\nLast 10 emails sent by {u.username}")
print("=" * 100)
print()

for i, log in enumerate(logs, 1):
    attachments = log.meta.get('attachments', 0) if log.meta else 0
    print(f"{i}. To: {log.to_email}")
    print(f"   Time: {log.sent_at}")
    print(f"   Attachments: {attachments}")
    print(f"   Subject: {log.subject}")
    print()

print("=" * 100)
