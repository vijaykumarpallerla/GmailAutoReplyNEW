import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.models import GmailToken
from django.contrib.auth.models import User

print("="*60)
print("CHECKING DATABASE FOR GMAIL TOKENS")
print("="*60)

# Check users
users = User.objects.all()
print(f"\nTotal users in database: {users.count()}")
for u in users:
    print(f"  - {u.username} ({u.email})")

# Check tokens
tokens = GmailToken.objects.all()
print(f"\nTotal GmailTokens in database: {tokens.count()}")

if tokens.count() == 0:
    print("\n❌ NO TOKENS FOUND!")
    print("User must login again to create tokens")
else:
    for t in tokens:
        print(f"\n✅ Token found:")
        print(f"   User: {t.user.username}")
        print(f"   Access Token exists: {bool(t.access_token)}")
        print(f"   Access Token length: {len(t.access_token)} chars")
        print(f"   Refresh Token exists: {bool(t.refresh_token)}")
        print(f"   Refresh Token length: {len(t.refresh_token) if t.refresh_token else 0} chars")
        print(f"   Created: {t.created_at}")
        print(f"   Updated: {t.updated_at}")

print("\n" + "="*60)
