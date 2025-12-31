import os
import sys
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')

import django
django.setup()

import cloudinary
import cloudinary.api
from urllib.parse import urlparse

# Parse credentials
cloudinary_url = os.environ.get('CLOUDINARY_URL')
parsed = urlparse(cloudinary_url)
cloud_name = parsed.hostname
api_key = parsed.username
api_secret = parsed.password

print("[FIXING] Removing ACL restrictions from PDF files\n")

pdf_ids = [
    'rule_attachments/1/0/HVDC AND FACTS (PEAPS).pdf',
    'rule_attachments/1/0/HVDC_LECTURE NOTES-2025.pdf',
]

for pdf_id in pdf_ids:
    try:
        print(f"Updating: {pdf_id}")
        # Update the resource to remove access_control (set it to empty to allow public access)
        result = cloudinary.api.update(
            pdf_id,
            resource_type='raw',
            access_control=None,  # Clear ACL
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
        )
        print(f"  ✓ Updated successfully")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()

print("\n[DONE] ACL restrictions removed. Files should now be publicly accessible.")
