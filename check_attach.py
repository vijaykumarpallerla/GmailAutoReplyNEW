import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

print('=' * 80)
print('NEELAM - Recent Emails with Attachments')
print('=' * 80)

neelam = User.objects.get(username='neelam')
recent_neelam = ReplyLog.objects.filter(user=neelam).order_by('-id')[:5]

for log in recent_neelam:
    print(f'\nLog ID: {log.id}')
    print(f'  To: {log.to_email}')
    print(f'  Subject: {log.subject_key[:60] if log.subject_key else "N/A"}')
    print(f'  Rule ID: {log.rule_id}')
    if log.meta:
        attachments = log.meta.get('attachments', 0)
        print(f'  Attachments: {attachments}')

print('\n' + '=' * 80)
print('ARE (User 16) - Recent Emails')
print('=' * 80)

are = User.objects.get(username='are')
recent_are = ReplyLog.objects.filter(user=are).order_by('-id')[:5]

if recent_are.exists():
    for log in recent_are:
        print(f'\nLog ID: {log.id}')
        print(f'  To: {log.to_email}')
        print(f'  Subject: {log.subject_key[:60] if log.subject_key else "N/A"}')
        print(f'  Rule ID: {log.rule_id}')
        if log.meta:
            attachments = log.meta.get('attachments', 0)
            print(f'  Attachments: {attachments}')
else:
    print('\nNo emails sent by are yet!')

print(f'\nTotal emails sent by are: {ReplyLog.objects.filter(user=are).count()}')
