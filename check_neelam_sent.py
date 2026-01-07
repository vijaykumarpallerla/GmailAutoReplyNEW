import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

neelam = User.objects.get(username='neelam')
print(f"\nRecent emails sent by Neelam (User ID: {neelam.id})")
print("=" * 80)

# Get last 10 sent emails
recent_logs = ReplyLog.objects.filter(user=neelam).order_by('-id')[:10]

if recent_logs:
    for log in recent_logs:
        print(f"\nLog ID: {log.id}")
        print(f"  To: {log.to_email}")
        print(f"  Subject: {log.subject_key[:80] if log.subject_key else 'N/A'}")
        print(f"  Rule ID: {log.rule_id}")
        print(f"  ⏰ Sent: {log.sent_at}")
else:
    print("\nNo sent emails found for Neelam")

print(f"\n\nTotal emails sent by Neelam: {ReplyLog.objects.filter(user=neelam).count()}")
