import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

import cloudinary
import cloudinary.api
from auto_reply.models import UserProfile

# Get Neelam's credentials
user = UserProfile.objects.get(user__username='neelam')
api_key_parts = user.cloudinary_api_key.split(':')
cloud_name = api_key_parts[0]
api_key = api_key_parts[1]
api_secret = api_key_parts[2]

# Configure Cloudinary with Neelam's credentials
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
    secure=True
)

# Check the problematic PDF
public_id = 'rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1].pdf'

print("=" * 80)
print(f"Checking: {public_id}")
print("=" * 80)

try:
    result = cloudinary.api.resource(public_id, resource_type='raw')
    print(f"✓ File found in Cloudinary")
    print(f"  Public ID: {result.get('public_id')}")
    print(f"  Resource Type: {result.get('resource_type')}")
    print(f"  Type: {result.get('type')}")
    print(f"  Access Mode: {result.get('access_mode')}")
    print(f"  Access Control: {result.get('access_control')}")
    print(f"  Version: {result.get('version')}")
    print(f"  Created: {result.get('created_at')}")
    print(f"  Secure URL: {result.get('secure_url')}")
    
    # Try to download the file
    print("\n" + "=" * 80)
    print("Testing download...")
    print("=" * 80)
    
    import requests
    url = result.get('secure_url')
    response = requests.get(url)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ Downloaded {len(response.content)} bytes")
    else:
        print(f"  ✗ Failed: {response.text}")
    
except Exception as e:
    print(f"✗ Error: {e}")
