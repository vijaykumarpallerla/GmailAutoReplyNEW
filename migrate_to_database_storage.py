"""
Migrate existing Cloudinary attachments to database storage.
This downloads all files from Cloudinary and stores them as base64 in the database.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule, User
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials, CloudinaryStorage
import base64

print("=" * 80)
print("MIGRATING CLOUDINARY ATTACHMENTS TO DATABASE STORAGE")
print("=" * 80)

users = User.objects.filter(autoreplyrule__isnull=False).distinct()
total_files = 0
migrated_files = 0
failed_files = 0

for user in users:
    print(f"\nUser: {user.username}")
    print("-" * 80)
    
    # Set up Cloudinary storage for this user
    storage = CloudinaryStorage()
    cloud, key, secret = get_user_cloudinary_credentials(user)
    
    if not cloud or not key:
        print(f"  ⚠ No Cloudinary credentials - skipping")
        continue
    
    storage.set_user_credentials(user)
    
    rules = AutoReplyRule.objects.filter(user=user)
    
    for rule in rules:
        for action in rule.actions.filter(action_type='send_email'):
            attachments = action.attachments or []
            if not attachments:
                continue
            
            print(f"\n  Rule: {rule.rule_name} (ID {rule.id})")
            
            migrated_attachments = []
            needs_save = False
            
            for att in attachments:
                total_files += 1
                
                # Check if already migrated (has 'content' field)
                if att.get('content'):
                    print(f"    ✓ Already in database: {att.get('name')}")
                    migrated_attachments.append(att)
                    continue
                
                # Need to migrate from Cloudinary
                path = att.get('path')
                name = att.get('name')
                
                if not path:
                    print(f"    ✗ No path for: {name}")
                    failed_files += 1
                    continue
                
                try:
                    # Download from Cloudinary
                    with storage.open(path, 'rb') as f:
                        content = f.read()
                    
                    # Convert to base64
                    content_base64 = base64.b64encode(content).decode('utf-8')
                    
                    # Update attachment
                    migrated_att = {
                        'group': att.get('group'),
                        'label': att.get('label'),
                        'name': name,
                        'size': att.get('size') or len(content),
                        'content_type': att.get('content_type'),
                        'content': content_base64,
                        # Keep old path for reference
                        'old_path': path,
                    }
                    
                    migrated_attachments.append(migrated_att)
                    migrated_files += 1
                    needs_save = True
                    print(f"    ✓ Migrated: {name} ({len(content)} bytes → {len(content_base64)} base64 chars)")
                    
                except Exception as e:
                    print(f"    ✗ Failed: {name} - {e}")
                    failed_files += 1
                    # Keep original attachment
                    migrated_attachments.append(att)
            
            if needs_save:
                action.attachments = migrated_attachments
                action.save(update_fields=['attachments'])
                print(f"    💾 Saved {len(migrated_attachments)} attachments to database")

print("\n" + "=" * 80)
print("MIGRATION SUMMARY")
print("=" * 80)
print(f"Total files found: {total_files}")
print(f"Successfully migrated: {migrated_files}")
print(f"Failed: {failed_files}")
print(f"Already in database: {total_files - migrated_files - failed_files}")
print("\n✓ Migration complete!")
print("=" * 80)
