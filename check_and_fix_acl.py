import os
import sys
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')

import django
django.setup()

import cloudinary
import cloudinary.api
from urllib.parse import urlparse
import json

# Parse credentials
cloudinary_url = os.environ.get('CLOUDINARY_URL')
parsed = urlparse(cloudinary_url)
cloud_name = parsed.hostname
api_key = parsed.username
api_secret = parsed.password

print("[CHECK] Checking ACL status of PDF files\n")

pdf_ids = [
    'rule_attachments/1/0/HVDC AND FACTS (PEAPS).pdf',
    'rule_attachments/1/0/HVDC_LECTURE NOTES-2025.pdf',
    'rule_attachments/1/0/HVDC ASSIGNMENT_2.docx',  # Compare with working file
]

for pdf_id in pdf_ids:
    try:
        print(f"\n{pdf_id}:")
        resource = cloudinary.api.resource(
            pdf_id,
            resource_type='raw',
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
        )
        print(f"  access_control: {resource.get('access_control', 'NOT SET')}")
        print(f"  public_id: {resource.get('public_id')}")
        print(f"  bytes: {resource.get('bytes')}")
    except Exception as e:
        print(f"  Error: {e}")

# Try deleting and re-uploading the PDF as public
print("\n\n[ATTEMPT] Re-uploading PDFs with correct settings")

try:
    print("\nDeleting PDF1...")
    cloudinary.uploader.destroy(
        'rule_attachments/1/0/HVDC AND FACTS (PEAPS).pdf',
        resource_type='raw',
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
    )
    print("  Deleted successfully")
except Exception as e:
    print(f"  Error: {e}")

try:
    print("\nDeleting PDF2...")
    cloudinary.uploader.destroy(
        'rule_attachments/1/0/HVDC_LECTURE NOTES-2025.pdf',
        resource_type='raw',
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
    )
    print("  Deleted successfully")
except Exception as e:
    print(f"  Error: {e}")

print("\n[DONE] Ready for new uploads")
