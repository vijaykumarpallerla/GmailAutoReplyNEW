import os
import sys
import django

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gmail_auto_reply.settings")
django.setup()

from django.conf import settings
from django.db import connection
from auto_reply.models import RuleAction

def prove_config():
    db_settings = settings.DATABASES['default']
    print(f"--- DATABASE CONFIGURATION ---")
    print(f"ENGINE: {db_settings['ENGINE']}")
    # Masking password, showing host
    print(f"NAME: {db_settings['NAME']}")
    print(f"HOST: {db_settings.get('HOST', 'Not set (SQLite?)')}")
    
    print(f"\n--- DATA STORAGE PROOF ---")
    try:
        total = 0
        with_content = 0
        without_content = 0
        
        # We need to iterate carefully as some JSON might be malformed or empty
        actions = RuleAction.objects.filter(attachments__isnull=False).order_by('-id')[:20]
        print(f"Checking last {actions.count()} actions (closest to present)...")

        for action in actions:
            atts = action.attachments
            if not atts or not isinstance(atts, list):
                continue
            
            total += 1
            # Check if ANY attachment in the list has 'content'
            has_content = any('content' in a for a in atts)
            
            if has_content:
                with_content += 1
                for a in atts:
                    if 'content' in a:
                        print(f"  [Found Base64 Data] User: '{action.rule.user.username}' | Rule: '{action.rule.rule_name}' | File: '{a.get('name')}' (Size: {len(a['content'])} bytes)")
                        break
            else:
                without_content += 1
                
        print(f"Total actions analyzed: {total}")
        print(f"Actions WITH 'content' (Base64 in DB): {with_content}")
        print(f"Actions WITHOUT 'content' (Path ref only): {without_content}")
        
        if with_content > 0:
            print("VERDICT: YES, file contents ARE stored in the database.")
        else:
            print("VERDICT: NO, file contents are NOT in the database (only paths).")

    except Exception as e:
        print(f"Error querying DB: {e}")

    print(f"\n--- CONNECTED USERS (GmailToken) ---")
    try:
        from auto_reply.models import GmailToken
        tokens = GmailToken.objects.select_related('user').all()
        print(f"Total connected users: {tokens.count()}")
        for t in tokens:
            print(f" - {t.user.username} ({t.user.email})")
            
    except Exception as e:
        print(f"Error list users: {e}")

if __name__ == "__main__":
    prove_config()
