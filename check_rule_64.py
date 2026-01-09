import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule

# Get rule 64 for Neelam
rule = AutoReplyRule.objects.get(id=64)

print("=" * 80)
print(f"Rule: {rule.rule_name} (ID {rule.id})")
print("=" * 80)

# Check the action
action = rule.actions.filter(action_type='send_email').first()

if action and action.attachments:
    print(f"\nAttachments in database: {len(action.attachments)}\n")
    
    for i, att in enumerate(action.attachments, 1):
        print(f"{i}. {att.get('name')}")
        print(f"   Path: {att.get('path')}")
        print(f"   Size: {att.get('size')} bytes")
        print()
else:
    print("No attachments found")
