import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
django.setup()

from django.contrib.auth.models import User
from auto_reply.models import AutoReplyRule, RuleCondition

vishnu = User.objects.get(username='vishnu')
print(f"\nChecking rules for Vishnu (User ID: {vishnu.id})")
print("=" * 60)

for rule in AutoReplyRule.objects.filter(user=vishnu):
    conditions = RuleCondition.objects.filter(rule=rule)
    condition_values = [c.value for c in conditions]
    
    # Check if this is the Python Developer rule
    for cond_value in condition_values:
        if 'python' in cond_value.lower() and 'developer' in cond_value.lower():
            print(f"\n✓ Python Developer Rule Found!")
            print(f"  Rule ID: {rule.id}")
            print(f"  Enabled: {'YES ✓' if rule.enabled else 'NO ✗'}")
            print(f"  Workspace: {rule.workspace}")
            print(f"  Conditions: {condition_values}")
            break
