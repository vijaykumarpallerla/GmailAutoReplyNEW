import os
import sys
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')

import django
django.setup()

import cloudinary.uploader
from urllib.parse import urlparse

# Parse credentials
cloudinary_url = os.environ.get('CLOUDINARY_URL')
parsed = urlparse(cloudinary_url)
cloud_name = parsed.hostname
api_key = parsed.username
api_secret = parsed.password

print("[CLEANUP] Deleting private PDFs from Cloudinary\n")

pdf_ids = [
    'rule_attachments/1/0/HVDC AND FACTS (PEAPS).pdf',
    'rule_attachments/1/0/HVDC_LECTURE NOTES-2025.pdf',
]

for pdf_id in pdf_ids:
    try:
        print(f"Deleting: {pdf_id}")
        cloudinary.uploader.destroy(
            pdf_id,
            resource_type='raw',
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
        )
        print(f"  ✓ Deleted")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n[DONE] Cloudinary cleaned up")
