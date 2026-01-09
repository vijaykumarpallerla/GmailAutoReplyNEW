import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

import cloudinary
import cloudinary.api
from dotenv import load_dotenv

load_dotenv()

shared_url = os.getenv('CLOUDINARY_URL')
from urllib.parse import urlparse
parsed = urlparse(shared_url)

cloudinary.config(
    cloud_name=parsed.hostname,
    api_key=parsed.username,
    api_secret=parsed.password,
    secure=True
)

print("=" * 80)
print("Checking if missing files exist in SHARED cloud")
print("=" * 80)

files_to_check = [
    ('rule_attachments/64/0/K Maruthamuthu_Guidewire_developer[1].docx', 'K Maruthamuthu'),
    ('rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1] (1).docx', 'Madhuri'),
    ('rule_attachments/64/0/Dinesh K_Guidewire[1].docx', 'Dinesh'),
]

for public_id, label in files_to_check:
    print(f"\n{label}: {public_id}")
    try:
        resource = cloudinary.api.resource(public_id, resource_type='raw')
        print(f"  ✓ Found in SHARED cloud")
        print(f"    Created: {resource.get('created_at')}")
        print(f"    Size: {resource.get('bytes')} bytes")
        
        # Try download
        import requests
        response = requests.get(resource.get('secure_url'))
        print(f"    Download: {response.status_code}")
        
    except Exception as e:
        print(f"  ✗ Not in shared cloud: {e}")
