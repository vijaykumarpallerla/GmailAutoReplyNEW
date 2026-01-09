import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
os.environ['DISABLE_IN_APP_SCHEDULER'] = '1'

import django
django.setup()

from auto_reply.models import UserProfile

# Get Neelam's credentials
user = UserProfile.objects.get(user__username='neelam')
print(f"User: {user.user.username} ({user.user.email})")
print(f"Cloudinary API Key: {user.cloudinary_api_key}")

if user.cloudinary_api_key:
    parts = user.cloudinary_api_key.split(':')
    if len(parts) == 3:
        cloud, key, secret = parts
        print(f"\nParsed:")
        print(f"  Cloud Name: {cloud}")
        print(f"  API Key: {key[:8]}{'*' * (len(key) - 8)}")
        print(f"  API Secret: {'*' * len(secret)}")
        
        # Test with these credentials
        import cloudinary
        import cloudinary.api
        
        cloudinary.config(
            cloud_name=cloud,
            api_key=key,
            api_secret=secret,
            secure=True
        )
        
        print("\n" + "=" * 80)
        print("Testing authentication...")
        print("=" * 80)
        
        try:
            # Try to get account info
            result = cloudinary.api.ping()
            print(f"✓ Authentication successful!")
            print(f"  Response: {result}")
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
    else:
        print(f"✗ Invalid format (expected cloud:key:secret)")
else:
    print("✗ No Cloudinary API key set")
