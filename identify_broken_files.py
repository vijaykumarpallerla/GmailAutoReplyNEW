"""Report which files need re-upload due to 401 errors"""
import os
import django

os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
from auto_reply.models import AutoReplyRule, User
import cloudinary
import cloudinary.api
import requests

print("=" * 80)
print("CHECKING ALL FILES FOR 401 ERRORS")
print("=" * 80)

users_to_check = ['neelam']
problems = []

for username in users_to_check:
    user = User.objects.get(username=username)
    cloud, key, secret = get_user_cloudinary_credentials(user)
    
    if not cloud:
        continue
    
    cloudinary.config(
        cloud_name=cloud,
        api_key=key,
        api_secret=secret,
        secure=True
    )
    
    print(f"\nUser: {username} (cloud: {cloud})")
    print("-" * 80)
    
    rules = AutoReplyRule.objects.filter(user=user)
    
    for rule in rules:
        for action in rule.actions.filter(action_type='send_email'):
            attachments = action.attachments or []
            
            for att in attachments:
                path = att.get('path')
                name = att.get('name')
                
                if not path:
                    continue
                
                public_id = path.replace('\\', '/')
                
                try:
                    resource = cloudinary.api.resource(public_id, resource_type='raw')
                    url = resource.get('secure_url')
                    
                    # Test download
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 401:
                        problems.append({
                            'user': username,
                            'rule_name': rule.rule_name,
                            'rule_id': rule.id,
                            'file_name': name,
                            'file_path': path
                        })
                        print(f"  ✗ {rule.rule_name} (ID {rule.id}): {name} - 401 ERROR")
                    elif response.status_code == 200:
                        print(f"  ✓ {rule.rule_name} (ID {rule.id}): {name} - OK")
                    else:
                        print(f"  ? {rule.rule_name} (ID {rule.id}): {name} - Status {response.status_code}")
                        
                except Exception as e:
                    print(f"  ✗ {rule.rule_name} (ID {rule.id}): {name} - ERROR: {e}")

print("\n" + "=" * 80)
print(f"SUMMARY: {len(problems)} file(s) need re-upload")
print("=" * 80)

if problems:
    print("\nFiles that need re-upload:")
    for p in problems:
        print(f"  • User {p['user']} → Rule '{p['rule_name']}' (ID {p['rule_id']})")
        print(f"    File: {p['file_name']}")
        print(f"    Action: User must delete and re-upload this attachment")
        print()
