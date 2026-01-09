"""Force cache invalidation for Neelam's PDF"""
import os
import django

os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
from auto_reply.models import UserProfile
import cloudinary.uploader
import cloudinary.api

# Get Neelam
user = UserProfile.objects.get(user__username='neelam').user

# Get her Cloudinary credentials
cloud, key, secret = get_user_cloudinary_credentials(user)

print(f"User: {user.username}")
print(f"Cloud: {cloud}")

# Configure Cloudinary
import cloudinary
cloudinary.config(
    cloud_name=cloud,
    api_key=key,
    api_secret=secret,
    secure=True
)

# The problematic PDF
public_id = 'rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1].pdf'

print("=" * 80)
print(f"Fixing: {public_id}")
print("=" * 80)

try:
    # First check current status
    resource = cloudinary.api.resource(public_id, resource_type='raw')
    print(f"Current access_mode: {resource.get('access_mode')}")
    print(f"Current type: {resource.get('type')}")
    
    # Update with invalidate=True to clear CDN cache
    result = cloudinary.uploader.explicit(
        public_id,
        type='upload',
        resource_type='raw',
        access_mode='public',
        invalidate=True  # Force CDN cache clear
    )
    
    print(f"✓ Updated! New access_mode: {result.get('access_mode')}")
    print(f"  New URL: {result.get('secure_url')}")
    
    # Test download
    import requests
    response = requests.get(result.get('secure_url'))
    print(f"\n  Download test: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✓ Success! Downloaded {len(response.content)} bytes")
    else:
        print(f"  ✗ Failed: {response.text}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
