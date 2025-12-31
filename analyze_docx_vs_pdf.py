import requests

# Simple test - directly trying the PDF again
# and checking for any workaround

urls_to_test = {
    'DOCX (working)': 'https://res.cloudinary.com/dowbh5rfy/raw/upload/v1767152535/rule_attachments/1/0/HVDC%20ASSIGNMENT_2.docx',
    'PDF (failing)': 'https://res.cloudinary.com/dowbh5rfy/raw/upload/v1767152761/rule_attachments/1/0/HVDC%20AND%20FACTS%20%28PEAPS%29.pdf',
}

print("[DEBUG] Analyzing difference between working DOCX and failing PDF\n")

for name, url in urls_to_test.items():
    print(f"\n{name}:")
    print(f"URL: {url}\n")
    
    # Get full response with all headers
    response = requests.get(url, allow_redirects=False, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Content-Length: {response.headers.get('Content-Length')}")
    print(f"Cache-Control: {response.headers.get('Cache-Control')}")
    print(f"x-cld-error: {response.headers.get('x-cld-error', 'NOT SET')}")
    
    # Check if there's a Location header (redirect)
    if 'Location' in response.headers:
        print(f"Location: {response.headers['Location']}")

# Try accessing via the base Cloudinary URL without the version
print("\n\n[TEST] Trying URL without version number:")
base_pdf_url = 'https://res.cloudinary.com/dowbh5rfy/raw/upload/rule_attachments/1/0/HVDC%20AND%20FACTS%20%28PEAPS%29.pdf'
try:
    response = requests.get(base_pdf_url, timeout=10)
    print(f"Status: {response.status_code}, Size: {len(response.content)} bytes")
except Exception as e:
    print(f"Failed: {e}")

# Try accessing via file name only (latest version)
print("\n[TEST] Trying with just filename:")
latest_pdf_url = 'https://res.cloudinary.com/dowbh5rfy/raw/upload/rule_attachments/1/0/HVDC%20AND%20FACTS%20%28PEAPS%29.pdf?_a=foo'
try:
    response = requests.get(latest_pdf_url, timeout=10)
    print(f"Status: {response.status_code}, Size: {len(response.content)} bytes")
except Exception as e:
    print(f"Failed: {e}")
