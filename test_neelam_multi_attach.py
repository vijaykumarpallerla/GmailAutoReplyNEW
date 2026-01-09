"""Test Neelam's Guidewire rule attachment processing"""
import os
import django

os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import AutoReplyRule
from django.core.files.storage import storages
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
import cloudinary.api

default_storage = storages['default']

u = User.objects.get(username='neelam')
rule = AutoReplyRule.objects.get(id=64)  # Guidewire Developers with 3 attachments
action = rule.actions.filter(action_type='send_email').first()

print(f"Rule: {rule.rule_name} (ID {rule.id})")
print(f"Attachments in DB: {len(action.attachments or [])}\n")

# Set user credentials
if hasattr(default_storage, 'set_user_credentials'):
    default_storage.set_user_credentials(u)

cloud, key, secret = get_user_cloudinary_credentials(u)
print(f"Using Cloudinary: {cloud}\n")

print("="*80)
print("TESTING ATTACHMENT PROCESSING (simulating send logic)")
print("="*80 + "\n")

attached_count = 0
for i, att in enumerate(action.attachments or [], 1):
    path = att.get('path')
    name = att.get('name')
    ctype = att.get('content_type')
    
    print(f"[{i}] Processing: {name}")
    print(f"    Path: {path}")
    print(f"    Content-Type: {ctype}")
    
    # Check existence
    try:
        exists = default_storage.exists(path)
        print(f"    Exists check: {exists}")
        
        if exists:
            # Try to open and get size
            with default_storage.open(path, 'rb') as fh:
                content = fh.read()
            print(f"    Downloaded: {len(content)} bytes")
            attached_count += 1
            print(f"    ✓ Would attach file #{attached_count}")
        else:
            print(f"    ✗ File not found in storage")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    print()

print("="*80)
print(f"RESULT: {attached_count} of {len(action.attachments or [])} attachments would be sent")
print("="*80)
