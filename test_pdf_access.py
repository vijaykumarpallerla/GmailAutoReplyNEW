import requests

# Try the HTTP version (not HTTPS) for the PDF
http_url = 'http://res.cloudinary.com/dowbh5rfy/raw/upload/v1767152761/rule_attachments/1/0/HVDC%20AND%20FACTS%20%28PEAPS%29.pdf'
https_url = 'https://res.cloudinary.com/dowbh5rfy/raw/upload/v1767152761/rule_attachments/1/0/HVDC%20AND%20FACTS%20%28PEAPS%29.pdf'

print("[TEST] Checking both HTTP and HTTPS\n")

print(f"HTTP (no auth): {http_url}")
try:
    response = requests.get(http_url, timeout=10, allow_redirects=True)
    print(f"Status: {response.status_code}, Size: {len(response.content)} bytes\n")
except Exception as e:
    print(f"Failed: {e}\n")

print(f"HTTPS (no auth): {https_url}")
try:
    response = requests.get(https_url, timeout=10, allow_redirects=True)
    print(f"Status: {response.status_code}, Size: {len(response.content)} bytes\n")
except Exception as e:
    print(f"Failed: {e}\n")

print(f"HTTPS with ?dl=1: {https_url}?dl=1")
try:
    response = requests.get(https_url + '?dl=1', timeout=10, allow_redirects=True)
    print(f"Status: {response.status_code}, Size: {len(response.content)} bytes\n")
except Exception as e:
    print(f"Failed: {e}\n")

# Try headers that might help
print(f"HTTPS with custom headers:")
try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(https_url, timeout=10, allow_redirects=True, headers=headers)
    print(f"Status: {response.status_code}, Size: {len(response.content)} bytes\n")
except Exception as e:
    print(f"Failed: {e}\n")

# Check response details on 401
print(f"Detailed 401 response:")
try:
    response = requests.get(https_url, timeout=10, allow_redirects=False)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text[:200]}")
except Exception as e:
    print(f"Failed: {e}")
