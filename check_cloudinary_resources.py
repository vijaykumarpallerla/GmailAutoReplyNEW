import os
import sys
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')

import django
django.setup()

import cloudinary
import cloudinary.api
from urllib.parse import urlparse

# Parse credentials from CLOUDINARY_URL
cloudinary_url = os.environ.get('CLOUDINARY_URL')
parsed = urlparse(cloudinary_url)
cloud_name = parsed.hostname
api_key = parsed.username
api_secret = parsed.password

print(f"[DEBUG] Testing Cloudinary API access")
print(f"[DEBUG] Cloud: {cloud_name}")

# Test getting resources
try:
    resources = cloudinary.api.resources(
        resource_type='raw',
        type='upload',
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        prefix='rule_attachments/1/0/',
        max_results=50
    )
    
    print(f"\n[DEBUG] Found {len(resources['resources'])} resources in rule_attachments/1/0/:")
    for res in resources['resources']:
        print(f"\n  Resource: {res['public_id']}")
        print(f"    Bytes: {res.get('bytes', 'N/A')}")
        print(f"    URL: {res.get('url', 'N/A')}")
        print(f"    Secure URL: {res.get('secure_url', 'N/A')}")
        print(f"    Access Control: {res.get('access_control', 'N/A')}")
except Exception as e:
    print(f"[ERROR] Failed to list resources: {e}")
    import traceback
    traceback.print_exc()
