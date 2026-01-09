"""Check Neelam's rule attachments count in DB"""
import os
import django

os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import AutoReplyRule

u = User.objects.get(username='neelam')
print(f"User: {u.username} ({u.email})")
print(f"Total rules: {AutoReplyRule.objects.filter(user=u).count()}\n")

rules = AutoReplyRule.objects.filter(user=u).order_by('id')
for r in rules:
    action = r.actions.filter(action_type='send_email').order_by('order', 'id').first()
    if not action:
        print(f"Rule: {r.rule_name} (ID {r.id}) - NO send_email action")
        continue
    
    atts = action.attachments or []
    print(f"Rule: {r.rule_name} (ID {r.id})")
    print(f"  Total attachments in DB: {len(atts)}")
    
    if len(atts) > 0:
        for i, att in enumerate(atts, 1):
            print(f"  [{i}] {att.get('name')} - path: {att.get('path')}")
    print()
