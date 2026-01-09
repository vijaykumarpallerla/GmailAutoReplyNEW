"""Try to delete and re-upload the PDF with explicit public access"""
import os
import django

os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from auto_reply.cloudinary_storage import get_user_cloudinary_credentials, CloudinaryStorage
from auto_reply.models import UserProfile, AutoReplyRule
import cloudinary.uploader
import cloudinary.api
import cloudinary

# Get Neelam
user_profile = UserProfile.objects.get(user__username='neelam')
user = user_profile.user
cloud, key, secret = get_user_cloudinary_credentials(user)

cloudinary.config(
    cloud_name=cloud,
    api_key=key,
    api_secret=secret,
    secure=True
)

# The problematic PDF
public_id = 'rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1].pdf'

print("=" * 80)
print("Strategy: Download → Delete → Re-upload with explicit public access")
print("=" * 80)

try:
    # Step 1: Download the current file
    print("\n1. Downloading current file...")
    resource = cloudinary.api.resource(public_id, resource_type='raw')
    
    # Use internal download (signed URL)
    import requests
    from cloudinary.utils import cloudinary_url
    signed_url, options = cloudinary_url(public_id, resource_type='raw', sign_url=True, type='upload')
    
    response = requests.get(signed_url)
    if response.status_code != 200:
        print(f"   ✗ Download failed: {response.status_code}")
        exit(1)
    
    file_data = response.content
    print(f"   ✓ Downloaded {len(file_data)} bytes")
    
    # Step 2: Delete the old file
    print("\n2. Deleting old file...")
    result = cloudinary.uploader.destroy(public_id, resource_type='raw', invalidate=True)
    print(f"   ✓ Deleted: {result.get('result')}")
    
    # Step 3: Re-upload with explicit public access
    print("\n3. Re-uploading with public access...")
    result = cloudinary.uploader.upload(
        file_data,
        public_id=public_id,
        resource_type='raw',
        type='upload',
        access_mode='public',  # Explicit public
        overwrite=True,
        invalidate=True
    )
    
    print(f"   ✓ Uploaded!")
    print(f"     Public ID: {result.get('public_id')}")
    print(f"     Access Mode: {result.get('access_mode')}")
    print(f"     URL: {result.get('secure_url')}")
    
    # Step 4: Test download
    print("\n4. Testing download...")
    test_response = requests.get(result.get('secure_url'))
    print(f"   Status: {test_response.status_code}")
    
    if test_response.status_code == 200:
        print(f"   ✓ SUCCESS! Downloaded {len(test_response.content)} bytes")
    else:
        print(f"   ✗ Still failing")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
