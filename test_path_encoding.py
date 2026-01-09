import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.cloudinary_storage import CloudinaryStorage, get_user_cloudinary_credentials
from auto_reply.models import UserProfile

user = UserProfile.objects.get(user__username='neelam').user
storage = CloudinaryStorage()
storage.set_user_credentials(user)

print("=" * 80)
print("Testing path encoding...")
print("=" * 80)

# Paths as stored in DB
db_paths = [
    'rule_attachments/64/0/K Maruthamuthu_Guidewire_developer[1].docx',
    'rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1] (1).docx',
    'rule_attachments/64/0/Dinesh K_Guidewire[1].docx',
]

for db_path in db_paths:
    print(f"\nDB Path: {db_path}")
    print(f"  URL encoded: {db_path.replace(' ', '%20')}")
    
    try:
        # Try with storage.exists()
        exists = storage.exists(db_path)
        print(f"  storage.exists(): {exists}")
        
        if not exists:
            # Try getting direct API info
            import cloudinary.api
            cloud, key, secret = get_user_cloudinary_credentials(user)
            import cloudinary
            cloudinary.config(
                cloud_name=cloud,
                api_key=key,
                api_secret=secret,
                secure=True
            )
            
            try:
                res = cloudinary.api.resource(db_path, resource_type='raw')
                print(f"  API direct call: ✓ Found (Size: {res.get('bytes')} bytes)")
            except Exception as e:
                print(f"  API direct call: ✗ {e}")
                
    except Exception as e:
        print(f"  Error: {e}")
