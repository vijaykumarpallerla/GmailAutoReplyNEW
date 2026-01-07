import os
print(f'DATABASE_URL env var: {os.environ.get("DATABASE_URL", "NOT SET")}')
