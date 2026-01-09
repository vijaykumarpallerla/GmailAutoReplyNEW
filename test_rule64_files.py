"""Test if the 2 files in rule 64 can be accessed"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule, User
from django.core.files.storage import storages
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials

default_storage = storages['default']
user = User.objects.get(username='neelam')
rule = AutoReplyRule.objects.get(id=64)

# Set credentials
if hasattr(default_storage, 'set_user_credentials'):
    default_storage.set_user_credentials(user)

cloud, key, secret = get_user_cloudinary_credentials(user)
print(f"User: {user.username}")
print(f"Cloud: {cloud}")
print(f"Rule: {rule.rule_name} (ID {rule.id})")

action = rule.actions.filter(action_type='send_email').first()
if not action or not action.attachments:
    print("No attachments in rule")
    exit()

print(f"\nAttachments in DB: {len(action.attachments)}\n")
print("="*80)

success_count = 0
for i, att in enumerate(action.attachments, 1):
    path = att.get('path')
    name = att.get('name')
    
    print(f"\n[{i}] {name}")
    print(f"    Path: {path}")
    
    try:
        # Check exists
        exists = default_storage.exists(path)
        print(f"    Exists: {exists}")
        
        if exists:
            # Try download
            with default_storage.open(path, 'rb') as f:
                content = f.read()
            print(f"    Downloaded: {len(content)} bytes ✓")
            success_count += 1
        else:
            print(f"    ✗ File not found in Cloudinary")
    except Exception as e:
        print(f"    ✗ Error: {e}")

print("\n" + "="*80)
print(f"RESULT: {success_count} of {len(action.attachments)} files accessible")
print("="*80)
