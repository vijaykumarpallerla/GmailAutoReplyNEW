"""Check detailed access control and try admin-level fetch"""
import os
import django

os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
from auto_reply.models import UserProfile
import cloudinary.api
import cloudinary

# Get Neelam
user = UserProfile.objects.get(user__username='neelam').user
cloud, key, secret = get_user_cloudinary_credentials(user)

cloudinary.config(
    cloud_name=cloud,
    api_key=key,
    api_secret=secret,
    secure=True
)

public_id = 'rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1].pdf'

print("=" * 80)
print("Checking all access control settings...")
print("=" * 80)

try:
    # Get full resource info
    resource = cloudinary.api.resource(public_id, resource_type='raw', max_results=500)
    
    print(f"\nAll available fields:")
    for key, value in sorted(resource.items()):
        if key not in ['public_id', 'secure_url', 'url']:  # Skip long values we already know
            print(f"  {key:30s}: {value}")
    
    # Try to get content via download API
    print("\n" + "=" * 80)
    print("Attempting signed download...")
    print("=" * 80)
    
    # Method 1: Use cloudinary download URL with signature
    from cloudinary import CloudinaryResource
    asset = CloudinaryResource(public_id, resource_type='raw', type='upload')
    download_url = asset.build_url(sign_url=True, secure=True)
    
    print(f"  Signed URL: {download_url[:100]}...")
    
    import requests
    response = requests.get(download_url)
    print(f"  Status: {response.status_code}")
    
    if response.status_code != 200:
        # Method 2: Try with auth in headers
        print("\n  Trying with auth header...")
        auth = (key, secret)
        response2 = requests.get(resource['secure_url'], auth=auth)
        print(f"  Status with auth: {response2.status_code}")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
