import os
import urllib.parse
import uuid
import requests
import logging
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserProfile

logger = logging.getLogger(__name__)

# Providers configuration
PROVIDERS = {
    'google': {
        'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'userinfo_url': 'https://openidconnect.googleapis.com/v1/userinfo',
        'scopes': 'openid email profile',
        'client_id_setting': 'OAUTH_GOOGLE_CLIENT_ID',
        'client_secret_setting': 'OAUTH_GOOGLE_CLIENT_SECRET',
    },
    'github': {
        'auth_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo_url': 'https://api.github.com/user',
        'emails_url': 'https://api.github.com/user/emails',
        'scopes': 'read:user user:email',
        'client_id_setting': 'OAUTH_GITHUB_CLIENT_ID',
        'client_secret_setting': 'OAUTH_GITHUB_CLIENT_SECRET',
    }
}


def get_oauth_credentials(provider):
    config = PROVIDERS.get(provider)
    if not config:
        return None, None
    client_id = getattr(settings, config['client_id_setting'], os.getenv(config['client_id_setting'], ''))
    client_secret = getattr(settings, config['client_secret_setting'], os.getenv(config['client_secret_setting'], ''))
    return client_id, client_secret


def is_provider_enabled(provider):
    client_id, client_secret = get_oauth_credentials(provider)
    return bool(client_id and client_secret)


def get_authorization_url(provider, redirect_uri, state=None):
    config = PROVIDERS.get(provider)
    if not config:
        return None

    client_id, _ = get_oauth_credentials(provider)
    if not client_id:
        return None

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': config['scopes'],
    }
    if state:
        params['state'] = state

    return f"{config['auth_url']}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(provider, code, redirect_uri):
    config = PROVIDERS.get(provider)
    if not config:
        return None, "Proveedor no configurado"

    client_id, client_secret = get_oauth_credentials(provider)
    if not client_id or not client_secret:
        return None, f"Credenciales de OAuth no configuradas en .env para {provider}"

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    headers = {'Accept': 'application/json'}

    try:
        resp = requests.post(config['token_url'], data=data, headers=headers, timeout=10)
        resp_json = resp.json()
        access_token = resp_json.get('access_token')
        if not access_token:
            return None, resp_json.get('error_description') or resp_json.get('error') or "Fallo al obtener token de acceso"
        return access_token, None
    except Exception as e:
        logger.error(f"Error exchange_code_for_token for {provider}: {e}")
        return None, str(e)


def fetch_userinfo(provider, access_token):
    config = PROVIDERS.get(provider)
    if not config:
        return None, "Proveedor invalido"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }

    try:
        resp = requests.get(config['userinfo_url'], headers=headers, timeout=10)
        data = resp.json()

        if provider == 'google':
            return {
                'id': data.get('sub'),
                'email': data.get('email'),
                'username': data.get('name') or data.get('email', '').split('@')[0],
                'avatar_url': data.get('picture', ''),
            }, None
        elif provider == 'github':
            email = data.get('email')
            if not email and 'emails_url' in config:
                emails_resp = requests.get(config['emails_url'], headers=headers, timeout=10)
                if emails_resp.ok:
                    for e in emails_resp.json():
                        if e.get('primary') and e.get('verified'):
                            email = e.get('email')
                            break

            return {
                'id': str(data.get('id')),
                'email': email or f"{data.get('login')}@users.noreply.github.com",
                'username': data.get('login') or data.get('name'),
                'avatar_url': data.get('avatar_url', ''),
            }, None
    except Exception as e:
        logger.error(f"Error fetching userinfo for {provider}: {e}")
        return None, str(e)


def get_or_create_oauth_user(provider, userinfo):
    """
    Finds existing user by oauth_uid, or by email, or creates a new user with generated UID.
    """
    oauth_uid = str(userinfo.get('id'))
    email = userinfo.get('email', '').strip().lower()
    username = userinfo.get('username', '').strip()
    avatar_url = userinfo.get('avatar_url', '')

    # 1. Look up existing UserProfile with this oauth provider & id
    profile = UserProfile.objects.filter(oauth_provider=provider, oauth_uid=oauth_uid).select_related('user').first()
    if profile:
        return profile.user, False

    # 2. Look up existing User by email
    user = None
    if email:
        user = User.objects.filter(email=email).first()

    if user:
        # Link user profile with this provider
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.oauth_provider = provider
        profile.oauth_uid = oauth_uid
        if avatar_url and not profile.avatar_url:
            profile.avatar_url = avatar_url
        profile.save()
        return user, False

    # 3. Create brand new user
    base_username = username or (email.split('@')[0] if email else f"user_{provider}")
    candidate_username = base_username
    counter = 1
    while User.objects.filter(username=candidate_username).exists():
        candidate_username = f"{base_username}_{counter}"
        counter += 1

    # Create user with an unusable password (passwordless OAuth user)
    new_user = User.objects.create(
        username=candidate_username,
        email=email,
        is_active=True,
    )
    new_user.set_unusable_password()
    new_user.save()

    profile, _ = UserProfile.objects.get_or_create(user=new_user)
    profile.oauth_provider = provider
    profile.oauth_uid = oauth_uid
    if avatar_url:
        profile.avatar_url = avatar_url
    profile.save()

    return new_user, True
