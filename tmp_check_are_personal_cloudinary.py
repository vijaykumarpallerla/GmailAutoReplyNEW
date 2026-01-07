import os
import django
import cloudinary.api

# Disable in-app scheduler side effects while running this script
os.environ.setdefault('DISABLE_IN_APP_SCHEDULER', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import AutoReplyRule
from auto_reply.cloudinary_storage import get_user_cloudinary_credentials

u = User.objects.get(username="are")
cloud, key, secret = get_user_cloudinary_credentials(u)
print(f"User: {u.username} ({u.email})")
print(f"Personal Cloudinary: {cloud} key={key}")

rules = list(AutoReplyRule.objects.filter(user=u))
print(f"Total rules: {len(rules)}")
for r in rules:
    action = r.actions.filter(action_type="send_email").order_by("order", "id").first()
    atts = action.attachments if action else None
    print(f"\n=== Rule: {r.rule_name} ===")
    if not action:
        print("  (no send_email action)")
        continue
    print(f"  Attachments in DB: {len(atts or [])}")
    for att in (atts or []):
        path = att.get("path")
        name = att.get("name")
        ctype = att.get("content_type")
        print(f"  - {name}")
        print(f"    Path: {path}")
        print(f"    Type: {ctype}")
        if not path:
            print("    Missing path")
            continue
        try:
            res = cloudinary.api.resource(
                path.replace('\\', '/'),
                resource_type="raw",
                cloud_name=cloud,
                api_key=key,
                api_secret=secret,
            )
            created = res.get("created_at")
            size = res.get("bytes")
            print(f"    Found in personal ({cloud}) created={created} size={size}")
        except Exception as e:
            print(f"    Not found in personal: {e}")
