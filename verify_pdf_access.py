import os
import django
import cloudinary
import cloudinary.api

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

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

try:
    result = cloudinary.api.resource(public_id, resource_type='raw')
    print(f"✓ File found in Cloudinary")
    print(f"  Public ID: {result.get('public_id')}")
    print(f"  Resource Type: {result.get('resource_type')}")
    print(f"  Type: {result.get('type')}")
    print(f"  Access Mode: {result.get('access_mode')}")
    print(f"  Access Control: {result.get('access_control')}")
    print(f"  Secure URL: {result.get('secure_url')}")
    print(f"  URL: {result.get('url')}")
    
    # Try to get a fresh delivery URL
    delivery_url = cloudinary.CloudinaryResource(public_id, resource_type='raw').build_url()
    print(f"\n  Fresh delivery URL: {delivery_url}")
    
except Exception as e:
    print(f"✗ Error: {e}")
