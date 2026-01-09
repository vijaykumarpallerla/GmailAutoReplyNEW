"""
Run a test pull for Neelam only to see if emails matching rule 64 now send all 3 attachments
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from django.core.management import call_command

print("=" * 80)
print("Running gmail_pull for user: neelam")
print("=" * 80)

try:
    call_command('gmail_pull', '--user', 'neelam')
    print("\n✓ gmail_pull completed for neelam")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
