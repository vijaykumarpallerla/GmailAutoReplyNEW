"""Remove duplicate attachments from rule 64"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials, CloudinaryStorage
import cloudinary.uploader
import cloudinary

# Get rule 64
rule = AutoReplyRule.objects.get(id=64)
action = rule.actions.filter(action_type='send_email').first()

print("=" * 80)
print(f"CLEANING RULE 64: {rule.rule_name}")
print("=" * 80)

if not action or not action.attachments:
    print("No attachments found")
    exit(0)

original_count = len(action.attachments)
print(f"\nCurrent attachments: {original_count}")

# Keep track of unique files (by name, preferring originals without suffix)
seen_names = {}
cleaned_attachments = []

for att in action.attachments:
    name = att.get('name')
    path = att.get('path')
    
    # Extract base name (remove auto-generated suffix like _JEfkwl6, _3sEXHFD, etc.)
    base_name = name
    import re
    base_name = re.sub(r'_[A-Za-z0-9]{7}\.', '.', name)  # Remove _XXXXXXX suffix before extension
    
    if base_name not in seen_names:
        # First occurrence - keep it
        seen_names[base_name] = att
        cleaned_attachments.append(att)
        print(f"\n✓ KEEP: {name}")
        print(f"  Path: {path}")
    else:
        # Duplicate found
        print(f"\n✗ REMOVE: {name}")
        print(f"  Path: {path}")
        print(f"  (duplicate of: {seen_names[base_name].get('name')})")
        
        # Delete from Cloudinary
        try:
            user = rule.user
            cloud, key, secret = get_user_cloudinary_credentials(user)
            
            cloudinary.config(
                cloud_name=cloud,
                api_key=key,
                api_secret=secret,
                secure=True
            )
            
            public_id = path.replace('\\', '/')
            result = cloudinary.uploader.destroy(public_id, resource_type='raw')
            print(f"  Deleted from Cloudinary: {result.get('result')}")
        except Exception as e:
            print(f"  ⚠ Could not delete from Cloudinary: {e}")

# Update the action
print("\n" + "=" * 80)
print(f"UPDATING DATABASE")
print("=" * 80)

action.attachments = cleaned_attachments
action.save()

print(f"\n✓ Updated attachments: {original_count} → {len(cleaned_attachments)}")
print(f"\nFinal attachments for rule 64:")
for i, att in enumerate(cleaned_attachments, 1):
    print(f"  {i}. {att.get('name')} ({att.get('size')} bytes)")

print("\n" + "=" * 80)
print("✓ DONE! Rule 64 now has 3 attachments instead of 6")
print("=" * 80)
