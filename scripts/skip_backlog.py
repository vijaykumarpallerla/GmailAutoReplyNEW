
import os
import sys
import django
from googleapiclient.discovery import build

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.models import GmailToken, GmailSyncState
from auto_reply.gmail_service import _build_creds

def skip_backlog():
    tokens = GmailToken.objects.all()
    print(f"Checking {len(tokens)} users for backlog skipping...")

    for token in tokens:
        user = token.user
        print(f"\nProcessing user: {user.username}")
        
        try:
            creds = _build_creds(token)
            service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
            
            # 1. Get current profile to find the CURRENT historyId (pointer to "NOW")
            profile = service.users().getProfile(userId='me').execute()
            current_history_id = profile.get('historyId')
            
            if not current_history_id:
                print(f"FAILED: Could not fetch historyId for {user.username}")
                continue

            # 2. Update the sync state
            # This "fast-forwards" the pointer so the next pull only asks for changes AFTER this ID.
            state, _ = GmailSyncState.objects.get_or_create(user=user)
            old_id = state.last_history_id
            
            state.last_history_id = current_history_id
            state.save()
            
            print(f"SUCCESS: Skipped backlog for {user.username}.")
            print(f"  Old History ID: {old_id}")
            print(f"  New History ID: {current_history_id} (Jumped to NOW)")
            
        except Exception as e:
            print(f"ERROR: Failed to update {user.username}: {e}")

if __name__ == "__main__":
    skip_backlog()
