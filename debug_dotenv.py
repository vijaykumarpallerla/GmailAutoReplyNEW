from pathlib import Path
from dotenv import dotenv_values

env_file = Path('.') / '.env'
config = dotenv_values(env_file)

print("=== Dotenv parsed values ===")
for key, value in config.items():
    if value:
        print(f"{key}: {value[:50]}{'...' if len(value) > 50 else ''}")
    else:
        print(f"{key}: (empty)")
