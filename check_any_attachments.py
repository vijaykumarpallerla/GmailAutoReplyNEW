import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

are = User.objects.get(username='are')

# Check if any emails from 'are' have attachments
emails_with_attachments = []
for log in ReplyLog.objects.filter(user=are).order_by('-id')[:100]:
    if log.meta and log.meta.get('attachments', 0) > 0:
        emails_with_attachments.append(log)

print(f'Emails from ARE with attachments count > 0: {len(emails_with_attachments)}')

if emails_with_attachments:
    print('\nMost recent email WITH attachments:')
    log = emails_with_attachments[0]
    print(f'Log ID: {log.id}')
    print(f'Rule ID: {log.rule_id}')
    print(f'To: {log.to_email}')
    att_count = log.meta.get('attachments', 0)
    print(f'Attachments: {att_count}')
    print(f'Sent at: {log.sent_at}')
else:
    print('\nNO emails with attachments found in last 100 sent!')
    print('This means attachments have NEVER been successfully sent by ARE!')
