import datetime
import jwt
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile

JWT_ALGORITHM = 'HS256'
DEFAULT_ACCESS_MINUTES = 60
DEFAULT_REFRESH_DAYS = 7


def _get_secret_key():
    return getattr(settings, 'SECRET_KEY', 'growup-secure-jwt-secret-key-fallback')


def generate_jwt_tokens(user):
    """
    Generates an Access Token and a Refresh Token using the user's UUID (uid).
    """
    profile, _ = UserProfile.objects.get_or_create(user=user)
    uid_str = str(profile.uid)
    now = datetime.datetime.now(datetime.timezone.utc)

    # Expirations from settings or defaults
    access_minutes = getattr(settings, 'JWT_ACCESS_MINUTES', DEFAULT_ACCESS_MINUTES)
    refresh_days = getattr(settings, 'JWT_REFRESH_DAYS', DEFAULT_REFRESH_DAYS)

    access_payload = {
        'uid': uid_str,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': profile.role,
        'token_type': 'access',
        'token_version': profile.jwt_token_version,
        'iat': now,
        'exp': now + datetime.timedelta(minutes=access_minutes),
    }

    refresh_payload = {
        'uid': uid_str,
        'user_id': user.id,
        'token_type': 'refresh',
        'token_version': profile.jwt_token_version,
        'iat': now,
        'exp': now + datetime.timedelta(days=refresh_days),
    }

    secret = _get_secret_key()
    access_token = jwt.encode(access_payload, secret, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, secret, algorithm=JWT_ALGORITHM)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': access_minutes * 60,
        'user': {
            'uid': uid_str,
            'username': user.username,
            'email': user.email,
            'role': profile.role,
        }
    }


def decode_jwt_token(token):
    """
    Decodes and validates a JWT token. Returns payload dict or raises error.
    """
    secret = _get_secret_key()
    return jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])


def get_user_from_jwt(token, expected_type='access'):
    """
    Verifies token, checks token_type and version against UserProfile,
    and returns the User instance if valid.
    """
    try:
        payload = decode_jwt_token(token)
    except jwt.ExpiredSignatureError:
        return None, "Token expirado"
    except jwt.InvalidTokenError as e:
        return None, f"Token invalido: {str(e)}"

    if payload.get('token_type') != expected_type:
        return None, f"Tipo de token incorrecto (esperado: {expected_type})"

    uid_str = payload.get('uid')
    if not uid_str:
        return None, "Token no contiene identificador uid"

    profile = UserProfile.objects.filter(uid=uid_str).select_related('user').first()
    if not profile or not profile.user.is_active:
        return None, "Usuario no existe o esta inactivo"

    if profile.jwt_token_version != payload.get('token_version', 1):
        return None, "Token revocado por cambio de seguridad"

    return profile.user, None


def jwt_required(view_func):
    """
    Decorator for API views requiring a valid JWT Bearer token in Authorization header.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'status': 'error',
                'message': 'Autenticacion requerida. Proporcione un token valido en Authorization: Bearer <token>'
            }, status=401)

        token = auth_header.split(' ', 1)[1].strip()
        user, error_msg = get_user_from_jwt(token, expected_type='access')
        if not user:
            return JsonResponse({
                'status': 'error',
                'message': error_msg or 'Acceso no autorizado'
            }, status=401)

        request.jwt_user = user
        return view_func(request, *args, **kwargs)

    return _wrapped_view
