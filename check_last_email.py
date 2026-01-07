import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

vishnu = User.objects.get(username='vishnu')
print(f"\nMost Recent Email from Vishnu (User ID: {vishnu.id})")
print("=" * 80)

# Get the most recent email
recent = ReplyLog.objects.filter(user=vishnu).order_by('-id').first()

if recent:
    print(f"\nLog ID: {recent.id}")
    print(f"To: {recent.to_email}")
    print(f"Subject: {recent.subject_key}")
    print(f"Thread ID: {recent.thread_id}")
    print(f"Rule ID: {recent.rule_id}")
    
    # Check for timestamp fields
    print(f"\n⏰ TIMESTAMPS:")
    for field in recent._meta.get_fields():
        if hasattr(recent, field.name):
            value = getattr(recent, field.name)
            if 'time' in field.name.lower() or 'date' in field.name.lower() or 'at' in field.name.lower():
                print(f"  {field.name}: {value}")
else:
    print("\nNo emails found for Vishnu")
