"""Investigate the Python rule email from Jan 6 that had 0 attachments"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import AutoReplyRule, RuleAction, ReplyLog
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
import cloudinary.api
from datetime import datetime

# Get the specific log entry
u = User.objects.get(email='vijayypallerla@gmail.com')
log = ReplyLog.objects.filter(
    user=u,
    to_email='y8610034@gmail.com',
    sent_at__contains='2026-01-06 16:55:48'
).first()

print("\n" + "="*100)
print("INVESTIGATION: Why Python rule sent 0 attachments on Jan 6, 16:55")
print("="*100 + "\n")

print(f"Email Details:")
print(f"  Sent: {log.sent_at}")
print(f"  To: {log.to_email}")
print(f"  Subject: {log.subject}")
print(f"  Attachments Actually Sent: {log.meta.get('attachments', 0) if log.meta else 0}")
print(f"  Rule: {log.rule.rule_name if log.rule else 'N/A'}")
print()

# Get the Python rule and its attachments NOW
python_rule = AutoReplyRule.objects.get(user=u, rule_name='Python ')
action = python_rule.actions.filter(action_type='send_email').first()

print(f"Python Rule Current State:")
print(f"  Attachments in DB now: {len(action.attachments or [])}")
print()

# Get credentials
user_cloud, user_key, user_secret = get_user_cloudinary_credentials(u)

from urllib.parse import urlparse
shared_url = os.environ.get('CLOUDINARY_URL')
parsed = urlparse(shared_url)
shared_cloud = parsed.hostname
shared_key = parsed.username
shared_secret = parsed.password

print("="*100)
print("CHECKING WHERE ATTACHMENTS EXIST NOW:")
print("="*100 + "\n")

for i, att in enumerate(action.attachments or [], 1):
    path = att.get('path')
    name = att.get('name')
    
    print(f"{i}. {name}")
    print(f"   Path: {path}")
    
    # Check in personal account and get upload date
    personal_found = False
    personal_date = None
    try:
        resource = cloudinary.api.resource(
            path.replace('\\', '/'),
            resource_type='raw',
            cloud_name=user_cloud,
            api_key=user_key,
            api_secret=user_secret
        )
        personal_found = True
        personal_date = resource.get('created_at')
        print(f"   ✅ PERSONAL ({user_cloud}): Uploaded {personal_date}")
    except Exception as e:
        print(f"   ❌ PERSONAL: Not found")
    
    # Check in shared account and get upload date
    shared_found = False
    shared_date = None
    try:
        resource = cloudinary.api.resource(
            path.replace('\\', '/'),
            resource_type='raw',
            cloud_name=shared_cloud,
            api_key=shared_key,
            api_secret=shared_secret
        )
        shared_found = True
        shared_date = resource.get('created_at')
        print(f"   ✅ SHARED ({shared_cloud}): Uploaded {shared_date}")
    except Exception as e:
        print(f"   ❌ SHARED: Not found")
    
    # Compare dates
    email_time = log.sent_at
    print(f"\n   Email sent at: {email_time}")
    
    if personal_found and personal_date:
        from dateutil import parser
        upload_time = parser.parse(personal_date)
        if upload_time < email_time:
            print(f"   ✅ Personal file existed BEFORE email (uploaded earlier)")
        else:
            print(f"   ❌ Personal file uploaded AFTER email (too late!)")
    
    if shared_found and shared_date:
        from dateutil import parser
        upload_time = parser.parse(shared_date)
        if upload_time < email_time:
            print(f"   ℹ️  Shared file existed BEFORE email")
        else:
            print(f"   ℹ️  Shared file uploaded AFTER email")
    
    print()

print("="*100)
print("\nCONCLUSION:")
print("If files existed in PERSONAL before email time but still sent 0 attachments,")
print("there was a download error. If files didn't exist yet, that's why 0 sent.")
print("="*100 + "\n")
