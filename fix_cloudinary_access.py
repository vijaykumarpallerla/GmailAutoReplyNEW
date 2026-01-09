"""Fix access mode for all attachment files in Cloudinary - one-time fix"""
import os
import django

os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import AutoReplyRule
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
import cloudinary.uploader
import cloudinary.api

def fix_user_attachments(user):
    """Fix access mode for all attachments belonging to a user"""
    cloud, key, secret = get_user_cloudinary_credentials(user)
    
    if not cloud or not key:
        print(f"  ⚠ Skipping {user.username}: no Cloudinary credentials")
        return 0, 0
    
    print(f"\n{'='*80}")
    print(f"User: {user.username} ({user.email})")
    print(f"Cloud: {cloud}")
    print(f"{'='*80}")
    
    rules = AutoReplyRule.objects.filter(user=user)
    total_files = 0
    fixed_files = 0
    
    for rule in rules:
        for action in rule.actions.filter(action_type='send_email'):
            attachments = action.attachments or []
            if not attachments:
                continue
            
            print(f"\nRule: {rule.rule_name} (ID {rule.id}) - {len(attachments)} attachments")
            
            for att in attachments:
                path = att.get('path')
                name = att.get('name')
                
                if not path:
                    continue
                
                total_files += 1
                public_id = path.replace('\\', '/')
                
                try:
                    # Get current resource info
                    resource = cloudinary.api.resource(
                        public_id,
                        resource_type='raw',
                        cloud_name=cloud,
                        api_key=key,
                        api_secret=secret,
                    )
                    
                    current_access = resource.get('access_mode', 'unknown')
                    
                    if current_access != 'public':
                        print(f"  🔧 Fixing: {name} (was: {current_access})")
                        
                        # Update to public access using explicit_update
                        cloudinary.uploader.explicit(
                            public_id,
                            resource_type='raw',
                            type='upload',
                            access_mode='public',
                            cloud_name=cloud,
                            api_key=key,
                            api_secret=secret,
                        )
                        
                        fixed_files += 1
                        print(f"     ✓ Fixed: now public")
                    else:
                        print(f"  ✓ OK: {name} (already public)")
                        
                except Exception as e:
                    print(f"  ✗ Error for {name}: {e}")
    
    return total_files, fixed_files

# Main execution
print("\n" + "="*80)
print("CLOUDINARY ACCESS MODE FIX - ONE-TIME OPERATION")
print("="*80)
print("\nThis will update all attachment files to have public access mode.")
print("Files will be accessible without authentication issues.\n")

# Get all users with rules
users_with_rules = User.objects.filter(autoreplyrule__isnull=False).distinct()

print(f"Found {users_with_rules.count()} users with rules\n")

grand_total_files = 0
grand_fixed_files = 0

for user in users_with_rules:
    try:
        total, fixed = fix_user_attachments(user)
        grand_total_files += total
        grand_fixed_files += fixed
    except Exception as e:
        print(f"\n✗ Error processing user {user.username}: {e}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total files checked: {grand_total_files}")
print(f"Files fixed: {grand_fixed_files}")
print(f"Already OK: {grand_total_files - grand_fixed_files}")
print("\n✓ Done! No more re-uploads needed.")
print("="*80 + "\n")
