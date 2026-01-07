import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import ReplyLog

vishnu = User.objects.get(username='vishnu')
print(f"\nRecent emails sent by Vishnu (User ID: {vishnu.id})")
print("=" * 80)

# Get last 10 sent emails
recent_logs = ReplyLog.objects.filter(user=vishnu).order_by('-id')[:10]

if recent_logs:
    for log in recent_logs:
        print(f"\nLog ID: {log.id}")
        print(f"  To: {log.to_email}")
        print(f"  Subject: {log.subject_key[:80]}...")
        print(f"  Rule ID: {log.rule_id}")
        print(f"  Created: {log.created_at if hasattr(log, 'created_at') else 'N/A'}")
else:
    print("\nNo sent emails found for Vishnu")

print(f"\n\nTotal emails sent by Vishnu: {ReplyLog.objects.filter(user=vishnu).count()}")
