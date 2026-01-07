"""Check last 15 emails sent by vijayypallerla with attachment details"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

u = User.objects.get(email='vijayypallerla@gmail.com')
logs = ReplyLog.objects.filter(user=u).order_by('-sent_at')[:15]

print(f"\n{'='*120}")
print(f"LAST 15 EMAILS SENT BY {u.username}")
print(f"{'='*120}\n")

for i, log in enumerate(logs, 1):
    attachments = log.meta.get('attachments', 0) if log.meta else 0
    rule_name = log.rule.rule_name if log.rule else 'N/A'
    
    print(f"{i}. To: {log.to_email}")
    print(f"   Time: {log.sent_at}")
    print(f"   Subject: {log.subject}")
    print(f"   Attachments Sent: {attachments}")
    print(f"   Rule: {rule_name}")
    print()

print(f"{'='*120}\n")
