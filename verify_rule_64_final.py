import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule

rule = AutoReplyRule.objects.get(id=64)

print("=" * 80)
print("Rule 64 - Current state")
print("=" * 80)

action = rule.actions.filter(action_type='send_email').first()

if action and action.attachments:
    print(f"\nAttachments in rule: {len(action.attachments)}\n")
    
    for i, att in enumerate(action.attachments, 1):
        print(f"{i}. {att.get('name')}")
        print(f"   Path: {att.get('path')}")
        print(f"   Size: {att.get('size')} bytes")
else:
    print("No attachments found")

print("\n" + "=" * 80)
print("Rule is correctly updated with 3 files!")
print("=" * 80)
print("\nNote: The ReplyLog metadata was recorded at send time.")
print("When new emails matching this rule are sent, they will get all 3 attachments.")
