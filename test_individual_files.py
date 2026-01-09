import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.cloudinary_storage import CloudinaryStorage, get_user_cloudinary_credentials
from auto_reply.models import AutoReplyRule, UserProfile
import requests

rule = AutoReplyRule.objects.get(id=64)
user_profile = UserProfile.objects.get(user__username='neelam')

# Set up storage with Neelam's credentials
storage = CloudinaryStorage()
storage.set_user_credentials(user_profile.user)

print("=" * 80)
print("Testing each attachment individually...")
print("=" * 80)

attachments = [
    ('rule_attachments/64/0/K Maruthamuthu_Guidewire_developer[1].docx', 'K Maruthamuthu'),
    ('rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1] (1).docx', 'Madhuri'),
    ('rule_attachments/64/0/Dinesh K_Guidewire[1].docx', 'Dinesh'),
]

for path, label in attachments:
    print(f"\n{label}: {path}")
    print("-" * 80)
    
    try:
        # Check existence
        exists = storage.exists(path)
        print(f"  Exists: {exists}")
        
        if exists:
            # Try to open/download
            f = storage._open(path)
            content = f.read()
            print(f"  Downloaded: {len(content)} bytes ✓")
            f.close()
        else:
            print(f"  ✗ File not found in Cloudinary")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "=" * 80)
