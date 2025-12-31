#!/usr/bin/env python
"""Check Django storage configuration"""
import os
import django
from dotenv import load_dotenv

# Load .env file
load_dotenv('.env')

print("=" * 60)
print("ENVIRONMENT VARIABLES CHECK")
print("=" * 60)
print(f"CLOUDINARY_URL set: {bool(os.environ.get('CLOUDINARY_URL'))}")
if os.environ.get('CLOUDINARY_URL'):
    cloudinary_url = os.environ.get('CLOUDINARY_URL')
    # Mask the secret
    if '@' in cloudinary_url:
        parts = cloudinary_url.split('@')
        masked_url = parts[0][:30] + '***' + '@' + parts[1]
        print(f"CLOUDINARY_URL value: {masked_url}")

print("\n" + "=" * 60)
print("DJANGO SETTINGS CHECK")
print("=" * 60)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage, storages

print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
print(f"STORAGES: {getattr(settings, 'STORAGES', 'Not set')}")
print(f"default_storage class: {type(default_storage).__name__}")
print(f"default_storage module: {type(default_storage).__module__}")

# Try to access the 'default' storage directly
try:
    explicit_storage = storages['default']
    print(f"storages['default'] class: {type(explicit_storage).__name__}")
    print(f"storages['default'] module: {type(explicit_storage).__module__}")
except Exception as e:
    print(f"Error accessing storages['default']: {e}")

print("\n" + "=" * 60)
print("CLOUDINARY MODULE CHECK")
print("=" * 60)
try:
    import cloudinary
    print("✓ cloudinary package installed")
    print(f"  cloud_name: {cloudinary.config().cloud_name}")
    print(f"  api_key: {cloudinary.config().api_key}")
except ImportError:
    print("✗ cloudinary package NOT installed")
except Exception as e:
    print(f"✗ cloudinary import error: {e}")

print("\n" + "=" * 60)
print("CLOUDINARY STORAGE CHECK")
print("=" * 60)
try:
    from auto_reply.cloudinary_storage import CloudinaryStorage
    print("✓ CloudinaryStorage class imported successfully")
    test_storage = CloudinaryStorage()
    print(f"  CloudinaryStorage instance created: {test_storage}")
except ImportError as e:
    print(f"✗ Failed to import CloudinaryStorage: {e}")
except Exception as e:
    print(f"✗ Error creating CloudinaryStorage: {e}")

print("\n" + "=" * 60)
