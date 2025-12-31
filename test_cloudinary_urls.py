#!/usr/bin/env python
"""Test Cloudinary URL accessibility."""
import requests
import os

# Test URLs from the debug logs
urls = {
    'DOCX (working)': 'https://res.cloudinary.com/dowbh5rfy/raw/upload/v1767152535/rule_attachments/1/0/HVDC%20ASSIGNMENT_2.docx',
    'PDF1 (failing)': 'https://res.cloudinary.com/dowbh5rfy/raw/upload/v1767152761/rule_attachments/1/0/HVDC%20AND%20FACTS%20%28PEAPS%29.pdf',
    'PDF2 (failing)': 'https://res.cloudinary.com/dowbh5rfy/raw/upload/v1767152764/rule_attachments/1/0/HVDC_LECTURE%20NOTES-2025.pdf',
}

# Cloudinary API credentials
api_key = '378252628684391'
api_secret = '-3PVWTGhuaXaAX9HY7jpclTzqsU'

print("[TEST] Testing Cloudinary URL accessibility\n")

for name, url in urls.items():
    print(f"Testing {name}:")
    print(f"  URL: {url}")
    
    # Test 1: Direct HTTP GET
    try:
        response = requests.get(url, timeout=10)
        print(f"  [Direct] Status: {response.status_code}, Size: {len(response.content)} bytes")
    except Exception as e:
        print(f"  [Direct] Failed: {e}")
    
    # Test 2: With HTTPBasicAuth
    try:
        from requests.auth import HTTPBasicAuth
        response = requests.get(url, timeout=10, auth=HTTPBasicAuth(api_key, api_secret))
        print(f"  [Auth] Status: {response.status_code}, Size: {len(response.content)} bytes")
    except Exception as e:
        print(f"  [Auth] Failed: {e}")
    
    # Test 3: Try downloading through the Python requests response
    try:
        response = requests.head(url, timeout=10)
        print(f"  [HEAD] Status: {response.status_code}")
    except Exception as e:
        print(f"  [HEAD] Failed: {e}")
    
    print()
