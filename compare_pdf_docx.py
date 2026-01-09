"""Compare PDF vs DOCX properties"""
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

# Compare PDF (fails) vs DOCX (works)
pdf_id = 'rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1].pdf'
docx_id = 'rule_attachments/64/0/K Maruthamuthu_Guidewire_developer[1].docx'

print("=" * 80)
print("COMPARISON: Working DOCX vs Failing PDF")
print("=" * 80)

for public_id, label in [(docx_id, "DOCX (WORKS)"), (pdf_id, "PDF (FAILS)")]:
    print(f"\n{label}: {public_id}")
    print("-" * 80)
    
    try:
        resource = cloudinary.api.resource(public_id, resource_type='raw')
        
        # Print all relevant fields
        for field in ['public_id', 'version', 'resource_type', 'type', 'format',
                      'access_mode', 'access_control', 'delivery_type', 
                      'created_at', 'bytes', 'url', 'secure_url']:
            value = resource.get(field, 'N/A')
            print(f"  {field:20s}: {value}")
        
        # Try download
        import requests
        response = requests.get(resource.get('secure_url'))
        print(f"  {'download_status':20s}: {response.status_code}")
        
    except Exception as e:
        print(f"  ERROR: {e}")
