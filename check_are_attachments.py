import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog, RuleAction

are = User.objects.get(username='are')

# Get the most recent email from are
recent = ReplyLog.objects.filter(user=are).order_by('-id').first()

if recent:
    print('Most Recent Email from ARE (User 16)')
    print('=' * 80)
    print(f'\nLog ID: {recent.id}')
    print(f'Rule ID: {recent.rule_id}')
    print(f'To: {recent.to_email}')
    print(f'Subject: {recent.subject_key}')
    print(f'Sent at: {recent.sent_at}')
    
    if recent.meta:
        print(f'\nMeta (Attachment Count): {recent.meta.get("attachments", 0)}')
    else:
        print('Meta: None')
    
    # Check if the rule has attachments
    if recent.rule:
        print(f'\n--- Rule Details ---')
        print(f'Rule Name: {recent.rule.rule_name}')
        
        actions = RuleAction.objects.filter(rule=recent.rule)
        for action in actions:
            if action.attachments:
                print(f'Rule HAS attachments configured: {len(action.attachments)} files')
                for att in action.attachments:
                    att_name = att.get('name', 'unknown')
                    print(f'  - {att_name}')
            else:
                print('Rule has NO attachments')
