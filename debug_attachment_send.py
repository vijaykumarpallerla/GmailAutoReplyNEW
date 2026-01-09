"""
Check which attachment failed during the most recent send
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule
from auto_reply.cloudinary_storage import CloudinaryStorage, get_user_cloudinary_credentials

rule = AutoReplyRule.objects.get(id=64)

print("=" * 80)
print("Testing each attachment from rule 64 - detailed")
print("=" * 80)

storage = CloudinaryStorage()
storage.set_user_credentials(rule.user)

attachments = [
    ('rule_attachments/64/0/K Maruthamuthu_Guidewire_developer[1].docx', 'K Maruthamuthu'),
    ('rule_attachments/64/0/Madhuri_KATA_Guidewire_Developer[1] (1).docx', 'Madhuri'),
    ('rule_attachments/64/0/Dinesh K_Guidewire[1].docx', 'Dinesh'),
]

success_count = 0

for i, (path, label) in enumerate(attachments, 1):
    print(f"\n{i}. {label}: {path}")
    print("-" * 80)
    
    try:
        # Test exists with cache (simulating what happens during email send)
        from auto_reply.gmail_service import _attachment_exists_with_cache
        
        exists = _attachment_exists_with_cache(path)
        print(f"  Exists (with cache): {exists}")
        
        if exists:
            # Try to open
            f = storage._open(path)
            content = f.read()
            print(f"  Download: {len(content)} bytes ✓")
            f.close()
            success_count += 1
        else:
            print(f"  ✗ File not found or exists check failed")
            
    except Exception as e:
        print(f"  ✗ Error during open: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print(f"RESULT: {success_count} of 3 attachments would be sent")
print("=" * 80)

if success_count < 3:
    print("\nDEBUG: Checking cache...")
    from auto_reply import gmail_service
    for path, label in attachments:
        if path in gmail_service._attachment_exists_cache:
            print(f"  {label}: CACHED = {gmail_service._attachment_exists_cache[path]}")
        else:
            print(f"  {label}: NOT CACHED")
