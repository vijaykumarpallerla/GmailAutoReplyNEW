"""Check which Cloudinary API credentials are actually being used for vijayypallerla"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials
from urllib.parse import urlparse

# Get user
u = User.objects.get(email='vijayypallerla@gmail.com')

print(f"\n{'='*100}")
print(f"Cloudinary API Key Analysis for: {u.username} ({u.email})")
print(f"{'='*100}\n")

# Get what's stored in database
try:
    stored_key = u.profile.cloudinary_api_key if hasattr(u, 'profile') else None
    print(f"1. DATABASE STORAGE:")
    print(f"   Stored key: {stored_key[:50]}..." if stored_key and len(stored_key) > 50 else f"   Stored key: {stored_key}")
    print()
except Exception as e:
    print(f"   Error reading profile: {e}\n")
    stored_key = None

# Get what the system will actually use (same logic as cloudinary_storage.py)
print(f"2. RUNTIME CREDENTIALS (what code actually uses):")
cloud_name, api_key, api_secret = get_user_cloudinary_credentials(u)
print(f"   Cloud Name: {cloud_name}")
print(f"   API Key: {api_key[:6]}***{api_key[-4:] if len(api_key) > 10 else '***'}")
print(f"   API Secret: {api_secret[:4]}***{api_secret[-4:] if len(api_secret) > 8 else '***'}")
print()

# Get shared/fallback credentials for comparison
print(f"3. SHARED CREDENTIALS (fallback):")
cloudinary_url = os.environ.get('CLOUDINARY_URL')
if cloudinary_url:
    parsed = urlparse(cloudinary_url)
    shared_cloud = parsed.hostname
    shared_key = parsed.username
    shared_secret = parsed.password
    print(f"   Cloud Name: {shared_cloud}")
    print(f"   API Key: {shared_key[:6]}***{shared_key[-4:] if len(shared_key) > 10 else '***'}")
    print(f"   API Secret: {shared_secret[:4]}***{shared_secret[-4:] if len(shared_secret) > 8 else '***'}")
else:
    print(f"   No CLOUDINARY_URL found in environment")
print()

# Comparison
print(f"4. VERDICT:")
if stored_key and cloud_name != shared_cloud:
    print(f"   ✅ Using PERSONAL Cloudinary account (not shared)")
    print(f"   ✅ User has independent 500 API calls/hour quota")
    print(f"   ✅ Cloud: {cloud_name} (user's own)")
elif stored_key and cloud_name == shared_cloud:
    print(f"   ⚠️  Using SHARED Cloudinary account (fallback)")
    print(f"   ⚠️  Personal key might be invalid or empty")
    print(f"   ⚠️  Cloud: {shared_cloud} (shared)")
else:
    print(f"   ⚠️  No personal key set - using SHARED account")
    print(f"   ⚠️  Shares 500 API calls/hour quota with other users")
    print(f"   ⚠️  Cloud: {shared_cloud} (shared)")

print(f"\n{'='*100}\n")
