from auto_reply.models import GmailToken
from django.contrib.auth.models import User

users = User.objects.all()
print(f'Total users: {users.count()}')

tokens = GmailToken.objects.all()
print(f'Total Gmail tokens: {tokens.count()}')

for t in tokens:
    print(f'\nUser: {t.user.username}')
    print(f'Access Token: {t.access_token[:50]}...')
    print(f'Refresh Token: {t.refresh_token[:50] if t.refresh_token else "NONE"}...')
    print(f'Created: {t.created_at}')
