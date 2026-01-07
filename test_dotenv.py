from pathlib import Path
import os

# Test what dotenv sees
env_path = Path(__file__).resolve().parent / '.env'
print(f"Looking for .env at: {env_path}")
print(f"File exists: {env_path.exists()}")

# Try dotenv
try:
    from dotenv import load_dotenv
    print("Attempting load_dotenv...")
    result = load_dotenv(env_path)
    print(f"load_dotenv result: {result}")
except Exception as e:
    print(f"dotenv failed: {e}")

# Check if DATABASE_URL is set
db_url = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL after load_dotenv: {db_url}")

# Try fallback parser
print("\nTrying fallback parser...")
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip())
        if k.strip() == 'DATABASE_URL':
            print(f"Set {k.strip()} = {v.strip()[:50]}...")

db_url = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL after fallback: {db_url}")
