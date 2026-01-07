import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import AutoReplyRule, RuleAction

print('=' * 80)
print('NEELAM - Rules with Attachments')
print('=' * 80)

neelam = User.objects.get(username='neelam')
rules_neelam = AutoReplyRule.objects.filter(user=neelam, enabled=True)

count = 0
for rule in rules_neelam:
    actions = RuleAction.objects.filter(rule=rule)
    for action in actions:
        if action.attachments:
            count += 1
            print(f'\nRule ID: {rule.id} - {rule.rule_name}')
            print(f'Attachments configured: YES')
            if isinstance(action.attachments, dict):
                print(f'Attachment details: {action.attachments}')
            else:
                print(f'Attachment details: {json.dumps(action.attachments, indent=2)}')

if count == 0:
    print('\nNo attachments configured in any rule')

print('\n' + '=' * 80)
print('ARE - Rules with Attachments')
print('=' * 80)

are = User.objects.get(username='are')
rules_are = AutoReplyRule.objects.filter(user=are, enabled=True)

count = 0
for rule in rules_are:
    actions = RuleAction.objects.filter(rule=rule)
    for action in actions:
        if action.attachments:
            count += 1
            print(f'\nRule ID: {rule.id} - {rule.rule_name}')
            print(f'Attachments configured: YES')
            if isinstance(action.attachments, dict):
                print(f'Attachment details: {action.attachments}')
            else:
                print(f'Attachment details: {json.dumps(action.attachments, indent=2)}')

if count == 0:
    print('\nNo attachments configured in any rule')
