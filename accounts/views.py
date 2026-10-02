import json
import secrets
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm, ProfileUpdateForm
from .jwt_auth import generate_jwt_tokens, get_user_from_jwt, jwt_required
from . import oauth_service


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Generate JWT credentials for session
            tokens = generate_jwt_tokens(user)
            request.session['jwt_access_token'] = tokens['access_token']
            messages.success(request, f"¡Bienvenido a GrowUp, {user.username}! Tu cuenta ha sido creada exitosamente.")
            return redirect('catalog:home')
        else:
            messages.error(request, "Por favor corrige los errores señalados a continuación.")
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'google_enabled': oauth_service.is_provider_enabled('google'),
        'github_enabled': oauth_service.is_provider_enabled('github'),
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            tokens = generate_jwt_tokens(user)
            request.session['jwt_access_token'] = tokens['access_token']
            messages.success(request, f"¡Bienvenido de vuelta, {user.username}!")
            next_url = request.GET.get('next') or 'catalog:home'
            return redirect(next_url)
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'google_enabled': oauth_service.is_provider_enabled('google'),
        'github_enabled': oauth_service.is_provider_enabled('github'),
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('catalog:home')


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', '')
            user.save()
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect('accounts:profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileUpdateForm(instance=profile, initial=initial)

    # Use single queries with only necessary fields
    user_reviews = request.user.reviews.select_related('user').only(
        'id', 'item_type', 'item_id', 'item_title', 'rating', 'headline', 'created_at'
    ).order_by('-created_at')[:10]
    
    user_novels = []
    if profile.is_author:
        user_novels = request.user.novels.only(
            'id', 'slug', 'title', 'cover_image', 'cover_url', 'status', 'views_count', 'created_at'
        ).order_by('-created_at')

    context = {
        'form': form,
        'profile': profile,
        'user_reviews': user_reviews,
        'user_novels': user_novels,
        'jwt_tokens': generate_jwt_tokens(request.user),
    }
    return render(request, 'accounts/profile.html', context)


# ==============================================================================
# OAuth 2.0 Views (Google & GitHub)
# ==============================================================================
def oauth_login_view(request, provider):
    if provider not in ('google', 'github'):
        return HttpResponseBadRequest("Proveedor OAuth no soportado")

    redirect_uri = request.build_absolute_uri(
        reverse('accounts:oauth_callback', kwargs={'provider': provider})
    )
    state = secrets.token_urlsafe(16)
    request.session[f'oauth_state_{provider}'] = state

    auth_url = oauth_service.get_authorization_url(provider, redirect_uri, state=state)
    if not auth_url:
        messages.warning(
            request,
            f"El proveedor {provider.capitalize()} no tiene credenciales configuradas en .env. "
            "Por favor configure OAUTH_GOOGLE_CLIENT_ID / OAUTH_GITHUB_CLIENT_ID."
        )
        return redirect('accounts:login')

    return redirect(auth_url)


def oauth_callback_view(request, provider):
    if provider not in ('google', 'github'):
        return HttpResponseBadRequest("Proveedor OAuth no soportado")

    state = request.GET.get('state')
    expected_state = request.session.get(f'oauth_state_{provider}')
    if not state or state != expected_state:
        messages.error(request, "Error de verificación CSRF en el flujo OAuth 2.0.")
        return redirect('accounts:login')

    code = request.GET.get('code')
    if not code:
        err = request.GET.get('error_description') or request.GET.get('error') or "Autorización denegada"
        messages.error(request, f"Error en OAuth 2.0: {err}")
        return redirect('accounts:login')

    redirect_uri = request.build_absolute_uri(
        reverse('accounts:oauth_callback', kwargs={'provider': provider})
    )
    access_token, token_err = oauth_service.exchange_code_for_token(provider, code, redirect_uri)
    if token_err:
        messages.error(request, f"No se pudo completar el intercambio OAuth: {token_err}")
        return redirect('accounts:login')

    userinfo, info_err = oauth_service.fetch_userinfo(provider, access_token)
    if info_err or not userinfo:
        messages.error(request, f"No se pudo obtener información del perfil OAuth: {info_err}")
        return redirect('accounts:login')

    user, created = oauth_service.get_or_create_oauth_user(provider, userinfo)
    login(request, user)

    # Issue JWT tokens
    tokens = generate_jwt_tokens(user)
    request.session['jwt_access_token'] = tokens['access_token']

    msg = f"¡Bienvenido a GrowUp! Tu cuenta ha sido creada con {provider.capitalize()}." if created else f"¡Bienvenido de vuelta, {user.username}!"
    messages.success(request, msg)
    return redirect('catalog:home')


# ==============================================================================
# JWT Authentication API Endpoints
# ==============================================================================
@csrf_exempt
def api_token_obtain_view(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método HTTP debe ser POST'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return JsonResponse({
            'status': 'error',
            'message': 'Campos username y password son obligatorios'
        }, status=400)

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({
            'status': 'error',
            'message': 'Credenciales inválidas'
        }, status=401)

    tokens = generate_jwt_tokens(user)
    return JsonResponse({
        'status': 'success',
        'message': 'Token generado con éxito',
        'tokens': tokens
    })


@csrf_exempt
def api_token_refresh_view(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método HTTP debe ser POST'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    refresh_token = data.get('refresh_token', '').strip()
    if not refresh_token:
        return JsonResponse({
            'status': 'error',
            'message': 'El campo refresh_token es obligatorio'
        }, status=400)

    user, err = get_user_from_jwt(refresh_token, expected_type='refresh')
    if not user:
        return JsonResponse({
            'status': 'error',
            'message': err or 'Token de refresco inválido o expirado'
        }, status=401)

    new_tokens = generate_jwt_tokens(user)
    return JsonResponse({
        'status': 'success',
        'access_token': new_tokens['access_token'],
        'expires_in': new_tokens['expires_in'],
        'token_type': 'Bearer'
    })


@jwt_required
def api_user_info_view(request):
    user = request.jwt_user
    profile = user.profile
    return JsonResponse({
        'status': 'success',
        'user': {
            'uid': str(profile.uid),
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': profile.role,
            'bio': profile.bio,
            'avatar_url': profile.avatar_url,
            'favorite_genres': profile.favorite_genres,
            'oauth_provider': profile.oauth_provider,
            'created_at': profile.created_at.isoformat(),
        }
    })

