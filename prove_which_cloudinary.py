"""Check where Guidewire rule attachments actually exist and which Cloudinary account was used"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import AutoReplyRule, RuleAction
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
import cloudinary.api

# Get user and rule
u = User.objects.get(email='vijayypallerla@gmail.com')
rule = AutoReplyRule.objects.get(user=u, rule_name='Guidewire')
action = rule.actions.filter(action_type='send_email').first()

print("\n" + "="*100)
print("GUIDEWIRE RULE ATTACHMENT INVESTIGATION")
print("="*100 + "\n")

print(f"Rule: {rule.rule_name}")
print(f"User: {u.username}")
print(f"Attachments in DB: {len(action.attachments or [])}")
print()

# Get user's personal credentials
user_cloud, user_key, user_secret = get_user_cloudinary_credentials(u)
print(f"User's Personal Cloudinary:")
print(f"  Cloud: {user_cloud}")
print(f"  Key: {user_key[:6]}***{user_key[-4:]}")
print()

# Get shared credentials
from urllib.parse import urlparse
shared_url = os.environ.get('CLOUDINARY_URL')
parsed = urlparse(shared_url)
shared_cloud = parsed.hostname
shared_key = parsed.username
shared_secret = parsed.password
print(f"Shared Cloudinary:")
print(f"  Cloud: {shared_cloud}")
print(f"  Key: {shared_key[:6]}***{shared_key[-4:]}")
print()

print("="*100)
print("CHECKING EACH ATTACHMENT:")
print("="*100 + "\n")

for i, att in enumerate(action.attachments or [], 1):
    path = att.get('path')
    name = att.get('name')
    
    print(f"{i}. {name}")
    print(f"   Path: {path}")
    
    # Check in user's personal account
    try:
        cloudinary.api.resource(
            path.replace('\\', '/'),
            resource_type='raw',
            cloud_name=user_cloud,
            api_key=user_key,
            api_secret=user_secret
        )
        print(f"   ✅ EXISTS in PERSONAL account ({user_cloud})")
    except Exception as e:
        print(f"   ❌ NOT FOUND in personal account: {str(e)[:50]}")
    
    # Check in shared account
    try:
        cloudinary.api.resource(
            path.replace('\\', '/'),
            resource_type='raw',
            cloud_name=shared_cloud,
            api_key=shared_key,
            api_secret=shared_secret
        )
        print(f"   ✅ EXISTS in SHARED account ({shared_cloud})")
    except Exception as e:
        print(f"   ❌ NOT FOUND in shared account: {str(e)[:50]}")
    
    print()

print("="*100)
print("\nVERDICT:")
print("If files exist in SHARED but not PERSONAL, then the download fell back to")
print("shared credentials because files were uploaded before personal key was set.")
print("="*100 + "\n")
