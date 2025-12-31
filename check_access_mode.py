import cloudinary
import cloudinary.api

cloudinary.config(
    cloud_name='dowbh5rfy',
    api_key='378252628684391',
    api_secret='rDbXVTtqTWw9hx3NXJIzjEfqI6k'
)

print("Checking recently uploaded files...")
resources = cloudinary.api.resources(type='upload', resource_type='raw', max_results=10)

for r in resources.get('resources', []):
    print(f"\nFile: {r.get('public_id')}")
    print(f"  Type: {r.get('type')}")
    print(f"  Access Mode: {r.get('access_mode', 'NOT SET')}")
    print(f"  Format: {r.get('format')}")
    print(f"  Bytes: {r.get('bytes')}")
    print(f"  URL: {r.get('secure_url')}")
