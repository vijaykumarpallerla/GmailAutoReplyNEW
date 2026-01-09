import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule
from auto_reply.cloudinary_storage import CloudinaryStorage, get_user_cloudinary_credentials
import cloudinary.api
import cloudinary

rule = AutoReplyRule.objects.get(id=64)

# The attachment that might have failed earlier
# The original PDF was: Madhuri_KATA_Guidewire_Developer[1].pdf
# But at the time of the send, was this replaced with a DOCX?

print("=" * 80)
print("Checking Cloudinary for Madhuri files...")
print("=" * 80)

cloud, key, secret = get_user_cloudinary_credentials(rule.user)

cloudinary.config(
    cloud_name=cloud,
    api_key=key,
    api_secret=secret,
    secure=True
)

# Search for all Madhuri files
import requests

files_to_check = [
    ('rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1].pdf', 'Original PDF'),
    ('rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1] (1).docx', 'New DOCX'),
]

for public_id, label in files_to_check:
    print(f"\n{label}: {public_id}")
    try:
        resource = cloudinary.api.resource(public_id, resource_type='raw')
        print(f"  ✓ Found - Version: {resource.get('version')}")
        print(f"    Size: {resource.get('bytes')} bytes")
        print(f"    Created: {resource.get('created_at')}")
        
        # Try to download
        response = requests.get(resource.get('secure_url'))
        print(f"    Download: {response.status_code}")
        
    except Exception as e:
        print(f"  ✗ Not found: {e}")
