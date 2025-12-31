#!/usr/bin/env python
"""Check if attachments are saved in database"""
import os
import django
from dotenv import load_dotenv

# Load .env
load_dotenv('.env')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.models import RuleAction
import json

print("=" * 80)
print("CHECKING RULE ACTIONS IN NEON DATABASE")
print("=" * 80)

# Get all rule actions with send_email type
actions = RuleAction.objects.filter(action_type='send_email').order_by('-id')[:5]

if not actions:
    print("\n❌ NO RULE ACTIONS FOUND IN DATABASE!")
else:
    for action in actions:
        print(f"\n{'=' * 80}")
        print(f"Action ID: {action.id}")
        print(f"Rule: {action.rule.rule_name} (ID: {action.rule.id})")
        print(f"Email Body Length: {len(action.email_body or '') } chars")
        
        if action.attachments:
            print(f"✅ ATTACHMENTS FOUND: {len(action.attachments)} files")
            for i, att in enumerate(action.attachments):
                print(f"\n  Attachment #{i+1}:")
                print(f"    Name: {att.get('name')}")
                print(f"    Path: {att.get('path')}")
                print(f"    Size: {att.get('size')} bytes")
                print(f"    Content Type: {att.get('content_type')}")
        else:
            print(f"❌ NO ATTACHMENTS in this action!")
        
        print(f"{'-' * 80}")

print("\n" + "=" * 80)
print("END OF REPORT")
print("=" * 80)
