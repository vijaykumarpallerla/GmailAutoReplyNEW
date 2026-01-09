import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import AutoReplyRule

rule = AutoReplyRule.objects.get(id=64)
action = rule.actions.filter(action_type='send_email').first()

print("=" * 80)
print("Database vs Cloudinary - File Status")
print("=" * 80)

if action and action.attachments:
    for att in action.attachments:
        name = att.get('name')
        path = att.get('path')
        size = att.get('size')
        
        print(f"\n{name}")
        print(f"  Path: {path}")
        print(f"  Size in DB: {size} bytes")
        
        # Check in personal cloud
        from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
        import cloudinary.api
        import cloudinary
        
        cloud, key, secret = get_user_cloudinary_credentials(rule.user)
        cloudinary.config(
            cloud_name=cloud,
            api_key=key,
            api_secret=secret,
            secure=True
        )
        
        public_id = path.replace('\\', '/')
        try:
            resource = cloudinary.api.resource(public_id, resource_type='raw')
            print(f"  Status: ✓ In personal cloud ({cloud})")
            print(f"    Cloudinary size: {resource.get('bytes')} bytes")
        except:
            print(f"  Status: ✗ NOT in personal cloud ({cloud})")
            
            # Check shared
            import os
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
            
            try:
                resource = cloudinary.api.resource(public_id, resource_type='raw')
                print(f"    ✓ Found in shared cloud ({parsed.hostname})")
            except:
                print(f"    ✗ NOT in either cloud")
