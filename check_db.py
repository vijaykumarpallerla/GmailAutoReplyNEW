#!/usr/bin/env python
import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.conf import settings

db = settings.DATABASES['default']
print(f"HOST: {db.get('HOST')}")
print(f"PORT: {db.get('PORT')}")
print(f"NAME: {db.get('NAME')}")
print(f"USER: {db.get('USER')}")
print(f"ENGINE: {db.get('ENGINE')}")
