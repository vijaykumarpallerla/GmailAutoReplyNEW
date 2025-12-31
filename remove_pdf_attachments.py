import os
import sys
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')

import django
django.setup()

from auto_reply.models import RuleAction
import json

print("[FIX] Removing inaccessible PDFs from database\n")

# Get the Python Developer rule action
try:
    action = RuleAction.objects.get(id=33)  # Python Developer action from the logs
    print(f"Found action: {action.rule.rule_name}\n")
    
    # Get current attachments
    current_attachments = action.attachments or []
    print(f"Current attachments ({len(current_attachments)}):")
    for i, att in enumerate(current_attachments):
        print(f"  {i+1}. {att['name']} ({att['size']} bytes)")
    
    # Filter out PDFs
    new_attachments = [att for att in current_attachments if not att['name'].endswith('.pdf')]
    
    print(f"\nFiltered attachments ({len(new_attachments)}):")
    for i, att in enumerate(new_attachments):
        print(f"  {i+1}. {att['name']} ({att['size']} bytes)")
    
    # Update the action
    action.attachments = new_attachments
    action.save()
    print(f"\n✓ Updated action - PDFs removed from database")
    print(f"✓ User can now re-upload PDFs and they will work correctly")
    
except RuleAction.DoesNotExist:
    print("Action not found - checking what actions exist:")
    for action in RuleAction.objects.all():
        print(f"  ID {action.id}: {action.rule.rule_name if action.rule else 'NO RULE'}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
