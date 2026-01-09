from django.core.management.base import BaseCommand
from auto_reply.models import AutoReplyRule, RuleAction


class Command(BaseCommand):
    help = 'List users, rules and attachment filenames stored in DB'

    def handle(self, *args, **options):
        rules = AutoReplyRule.objects.select_related('user').prefetch_related('actions').order_by('user__username', 'id')
        current_user = None
        for rule in rules:
            if current_user != rule.user.username:
                current_user = rule.user.username
                self.stdout.write(f"\nUser: {current_user}")
            self.stdout.write(f"  Rule: {rule.rule_name} (id={rule.id})")
            for action in rule.actions.all():
                atts = action.attachments or []
                if not atts:
                    self.stdout.write("    attachments: (none)")
                    continue
                self.stdout.write(f"    attachments: {len(atts)}")
                for att in atts:
                    name = att.get('name') or att.get('filename') or '(unnamed)'
                    ctype = att.get('content_type') or att.get('type') or 'unknown'
                    size = att.get('size')
                    has_content = 'content' in att and bool(att.get('content'))
                    info = f"{name} — {ctype}"
                    if size:
                        info += f" — {size} bytes"
                    if not has_content:
                        info += " — NO CONTENT STORED"
                    self.stdout.write(f"      - {info}")
