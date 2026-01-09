import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
from auto_reply.models import UserProfile
import cloudinary.search
import cloudinary

user = UserProfile.objects.get(user__username='neelam').user
cloud, key, secret = get_user_cloudinary_credentials(user)

cloudinary.config(
    cloud_name=cloud,
    api_key=key,
    api_secret=secret,
    secure=True
)

print("=" * 80)
print("ALL FILES in Neelam's Cloudinary for rule 64 path")
print("=" * 80)

try:
    # List all files with 'rule_attachments/64' prefix
    import cloudinary.api
    result = cloudinary.api.resources(resource_type='raw', type='upload', prefix='rule_attachments/64/', max_results=500)
    
    print(f"Found {len(result.get('resources', []))} files:\n")
    
    if result.get('resources'):
        for res in result['resources']:
            public_id = res.get('public_id')
            size = res.get('bytes')
            created = res.get('created_at')
            print(f"{public_id}")
            print(f"  Size: {size} bytes")
            print(f"  Created: {created}\n")
    else:
        print("No resources found")
        
except Exception as e:
    print(f"Error: {e}")
