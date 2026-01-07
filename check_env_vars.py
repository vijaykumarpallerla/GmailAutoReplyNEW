import os
from pathlib import Path

# Test what settings.py actually loads
print("=== Testing Environment Variable Loading ===")
print()

# Method 1: Check raw environment
print("1. Raw environment variables:")
print(f"   SOCIAL_GOOGLE_CLIENT_ID: {os.environ.get('SOCIAL_GOOGLE_CLIENT_ID', 'NOT SET')}")
print(f"   DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")
print()

# Method 2: Load from .env manually
from dotenv import load_dotenv
env_path = Path('.') / '.env'
print(f"2. Loading from {env_path}")
result = load_dotenv(env_path)
print(f"   load_dotenv result: {result}")
print(f"   SOCIAL_GOOGLE_CLIENT_ID: {os.environ.get('SOCIAL_GOOGLE_CLIENT_ID', 'NOT SET')}")
print()

# Method 3: Check what Django settings actually has
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.conf import settings
print("3. Django settings values:")
print(f"   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: {settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}")
print(f"   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: {settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET}")
print(f"   GMAIL_CLIENT_ID: {settings.GMAIL_CLIENT_ID}")
