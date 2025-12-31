from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import GmailToken

def restrict_email_domain(backend, details, response, *args, **kwargs):
    allowed_domains = getattr(settings, 'ALLOWED_EMAIL_DOMAINS', [])
    allowed_emails = getattr(settings, 'ALLOWED_EMAILS', [])
    
    # If no restrictions are set, allow everyone (or you could default to deny)
    if not allowed_domains and not allowed_emails:
        return

    email = details.get('email', '')
    request = kwargs.get('request')
    
    # Check specific emails
    if email in allowed_emails:
        return

    # Check domains
    if any(email.endswith(domain) for domain in allowed_domains):
        return

    return render(request, 'access_denied.html', status=403)

def save_gmail_token(backend, user, response, *args, **kwargs):
    """
    Pipeline step to save the Google OAuth2 token to the GmailToken model.
    This ensures we capture the refresh token during the initial login.
    """
    if backend.name != 'google-oauth2':
        return

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    if not access_token:
        return

    # Calculate expiry
    expiry = None
    if expires_in:
        expiry = timezone.now() + timedelta(seconds=expires_in)

    # Update or create the GmailToken
    token_obj, created = GmailToken.objects.get_or_create(user=user)
    token_obj.access_token = access_token
    
    # Only update refresh_token if we got a new one (it's not always sent)
    if refresh_token:
        token_obj.refresh_token = refresh_token
    
    if expiry:
        token_obj.token_expiry = expiry
        
    token_obj.save()
