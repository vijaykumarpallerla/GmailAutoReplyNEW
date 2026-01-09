import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

# Clear the attachment cache
from auto_reply import gmail_service

print("=" * 80)
print("Clearing attachment cache...")
print("=" * 80)

print(f"Cache before clear: {len(gmail_service._attachment_exists_cache)} items")

gmail_service._attachment_exists_cache.clear()
gmail_service._cache_expiry.clear()

print(f"Cache after clear: {len(gmail_service._attachment_exists_cache)} items")

# Now test
from auto_reply.models import AutoReplyRule

rule = AutoReplyRule.objects.get(id=64)
storage = __import__('auto_reply.cloudinary_storage', fromlist=['CloudinaryStorage']).CloudinaryStorage()
storage.set_user_credentials(rule.user)

print("\n" + "=" * 80)
print("Re-testing attachments with cleared cache...")
print("=" * 80)

attachments = [
    ('rule_attachments/64/0/K Maruthamuthu_Guidewire_developer[1].docx', 'K Maruthamuthu'),
    ('rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1] (1).docx', 'Madhuri'),
    ('rule_attachments/64/0/Dinesh K_Guidewire[1].docx', 'Dinesh'),
]

success_count = 0

for i, (path, label) in enumerate(attachments, 1):
    print(f"\n{i}. {label}")
    
    try:
        exists = gmail_service._attachment_exists_with_cache(path)
        print(f"   Exists: {exists}")
        
        if exists:
            f = storage._open(path)
            content = f.read()
            print(f"   Download: {len(content)} bytes ✓")
            f.close()
            success_count += 1
        else:
            print(f"   ✗ File not found")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")

print("\n" + "=" * 80)
print(f"RESULT: {success_count} of 3 attachments ready")
print("=" * 80)
