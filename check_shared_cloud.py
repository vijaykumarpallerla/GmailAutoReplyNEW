"""Check if PDF was uploaded to shared cloud instead of personal cloud"""
import os
import django

os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

import cloudinary
import cloudinary.api

print("=" * 80)
print("Checking PDF in SHARED Cloudinary account...")
print("=" * 80)

# Configure with SHARED credentials from environment
from dotenv import load_dotenv
load_dotenv()

shared_url = os.getenv('CLOUDINARY_URL')
if not shared_url:
    print("✗ No shared CLOUDINARY_URL in environment")
    exit(1)

from urllib.parse import urlparse
parsed = urlparse(shared_url)

cloudinary.config(
    cloud_name=parsed.hostname,
    api_key=parsed.username,
    api_secret=parsed.password,
    secure=True
)

print(f"Shared cloud: {parsed.hostname}")

public_id = 'rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1].pdf'

try:
    resource = cloudinary.api.resource(public_id, resource_type='raw')
    print(f"\n✓ PDF found in SHARED cloud!")
    print(f"  Created: {resource.get('created_at')}")
    print(f"  Bytes: {resource.get('bytes')}")
    print(f"  URL: {resource.get('secure_url')}")
    
    # Try download
    import requests
    response = requests.get(resource.get('secure_url'))
    print(f"\n  Download test: {response.status_code}")
    
    if response.status_code == 200:
        print(f"  ✓ Downloaded {len(response.content)} bytes from SHARED cloud")
        print("\n" + "=" * 80)
        print("SOLUTION: File is in shared cloud, not Neelam's personal cloud!")
        print("The user needs to re-upload this attachment so it goes to their personal cloud.")
        print("=" * 80)
    else:
        print(f"  ✗ Still 401 in shared cloud too")
        
except Exception as e:
    print(f"\n✗ PDF NOT in shared cloud: {e}")
    print("\nThis means the file is only in Neelam's personal cloud but has wrong ACL.")
    print("User must re-upload the file.")
