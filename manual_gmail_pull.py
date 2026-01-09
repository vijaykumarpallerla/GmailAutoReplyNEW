import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.gmail_service import gmail_pull_for_user
from auto_reply.models import GmailToken
from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*80)
print("MANUAL GMAIL PULL - Pull new emails NOW")
print("="*80)

tokens = GmailToken.objects.select_related('user').all()

if not tokens:
    print("❌ No connected Gmail accounts found")
else:
    print(f"\nFound {tokens.count()} connected Gmail account(s)\n")
    
    for token in tokens:
        user = token.user
        print(f"Pulling emails for: {user.username} ({user.email})...")
        
        try:
            result = gmail_pull_for_user(user)
            print(f"  ✅ Processed: {result['processed']}, Matched: {result['matched']}, Sent: {result['sent']}, Skipped: {result['skipped']}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

print("\n" + "="*80)
print("Pull complete! Check your email inbox for auto-replies.")
print("="*80 + "\n")
