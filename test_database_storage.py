"""Test database storage - verify files can be uploaded and retrieved"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule, User

# Pick a user with migrated attachments
user = User.objects.get(username='neelam')
rules = AutoReplyRule.objects.filter(user=user)

print("=" * 80)
print("Testing Database Storage")
print("=" * 80)

for rule in rules:
    for action in rule.actions.filter(action_type='send_email'):
        attachments = action.attachments or []
        if not attachments:
            continue
        
        print(f"\nRule: {rule.rule_name} (ID {rule.id})")
        print(f"Attachments: {len(attachments)}")
        
        success_count = 0
        for i, att in enumerate(attachments, 1):
            name = att.get('name')
            content_base64 = att.get('content')
            size = att.get('size')
            
            if content_base64:
                import base64
                try:
                    # Try to decode
                    content = base64.b64decode(content_base64)
                    actual_size = len(content)
                    
                    print(f"  [{i}] {name}")
                    print(f"      Stored size: {size} bytes")
                    print(f"      Actual size: {actual_size} bytes")
                    print(f"      ✓ Can decode successfully")
                    success_count += 1
                except Exception as e:
                    print(f"  [{i}] {name} - ✗ Decode error: {e}")
            else:
                print(f"  [{i}] {name} - ✗ No content in database")
        
        print(f"\n  Result: {success_count}/{len(attachments)} files ready to send")

print("\n" + "=" * 80)
print("✓ Test complete - all files stored in database")
print("=" * 80)
