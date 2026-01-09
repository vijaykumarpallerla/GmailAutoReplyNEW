"""Comprehensive audit of all rules for duplicates and missing files"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule, User
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
import cloudinary.api
import cloudinary
import requests

print("=" * 80)
print("COMPREHENSIVE AUDIT: ALL RULES FOR DUPLICATES & MISSING FILES")
print("=" * 80)

issues = {
    'duplicates': [],
    'missing_files': [],
    'access_errors': [],
}

# Get all users that have AutoReplyRules
users = User.objects.filter(autoreplyrule__isnull=False).distinct()

for user in users:
    try:
        cloud, key, secret = get_user_cloudinary_credentials(user)
        if not cloud or not key:
            continue
        
        cloudinary.config(
            cloud_name=cloud,
            api_key=key,
            api_secret=secret,
            secure=True
        )
        
        rules = AutoReplyRule.objects.filter(user=user)
        
        for rule in rules:
            action = rule.actions.filter(action_type='send_email').first()
            if not action or not action.attachments:
                continue
            
            # Check for duplicates
            seen_names = {}
            duplicates_in_rule = []
            
            for att in action.attachments:
                name = att.get('name')
                path = att.get('path')
                
                import re
                base_name = re.sub(r'_[A-Za-z0-9]{7}\.', '.', name)
                
                if base_name not in seen_names:
                    seen_names[base_name] = path
                else:
                    duplicates_in_rule.append({
                        'user': user.username,
                        'rule_name': rule.rule_name,
                        'rule_id': rule.id,
                        'file_name': name,
                        'base_name': base_name,
                        'path': path
                    })
            
            if duplicates_in_rule:
                for dup in duplicates_in_rule:
                    issues['duplicates'].append(dup)
            
            # Check for missing/error files
            for att in action.attachments:
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
                    
                    if response.status_code == 404:
                        issues['missing_files'].append({
                            'user': user.username,
                            'rule_name': rule.rule_name,
                            'rule_id': rule.id,
                            'file_name': name,
                            'path': path
                        })
                    elif response.status_code == 401:
                        issues['access_errors'].append({
                            'user': user.username,
                            'rule_name': rule.rule_name,
                            'rule_id': rule.id,
                            'file_name': name,
                            'path': path
                        })
                        
                except Exception as e:
                    if '404' in str(e):
                        issues['missing_files'].append({
                            'user': user.username,
                            'rule_name': rule.rule_name,
                            'rule_id': rule.id,
                            'file_name': name,
                            'path': path,
                            'error': str(e)
                        })
                    elif '401' in str(e):
                        issues['access_errors'].append({
                            'user': user.username,
                            'rule_name': rule.rule_name,
                            'rule_id': rule.id,
                            'file_name': name,
                            'path': path,
                            'error': str(e)
                        })
    
    except Exception as e:
        pass

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

if issues['duplicates']:
    print(f"\n⚠ DUPLICATES FOUND: {len(issues['duplicates'])}")
    print("-" * 80)
    for issue in issues['duplicates']:
        print(f"  User: {issue['user']}")
        print(f"  Rule: {issue['rule_name']} (ID {issue['rule_id']})")
        print(f"  File: {issue['file_name']}")
        print()
else:
    print("\n✓ No duplicates found")

if issues['missing_files']:
    print(f"\n✗ MISSING FILES (404): {len(issues['missing_files'])}")
    print("-" * 80)
    for issue in issues['missing_files']:
        print(f"  User: {issue['user']}")
        print(f"  Rule: {issue['rule_name']} (ID {issue['rule_id']})")
        print(f"  File: {issue['file_name']}")
        print()
else:
    print("\n✓ No missing files (404)")

if issues['access_errors']:
    print(f"\n✗ ACCESS ERRORS (401): {len(issues['access_errors'])}")
    print("-" * 80)
    for issue in issues['access_errors']:
        print(f"  User: {issue['user']}")
        print(f"  Rule: {issue['rule_name']} (ID {issue['rule_id']})")
        print(f"  File: {issue['file_name']}")
        print()
else:
    print("\n✓ No access errors (401)")

print("\n" + "=" * 80)
print(f"SUMMARY")
print("=" * 80)
total = len(issues['duplicates']) + len(issues['missing_files']) + len(issues['access_errors'])
print(f"Total issues found: {total}")

if total == 0:
    print("\n✓ All good! No issues detected in any rules.")
else:
    print(f"\n⚠ Action required:")
    if issues['duplicates']:
        print(f"  1. Run cleanup script to remove {len(issues['duplicates'])} duplicate(s)")
    if issues['missing_files']:
        print(f"  2. Users must re-upload {len(issues['missing_files'])} missing file(s)")
    if issues['access_errors']:
        print(f"  3. Users must re-upload {len(issues['access_errors'])} file(s) with access issues")
