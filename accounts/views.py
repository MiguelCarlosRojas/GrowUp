import json
import secrets
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
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
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        login_input = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Allow logging in with either username or email (case-insensitive)
        user_obj = None
        if '@' in login_input:
            user_obj = User.objects.filter(email__iexact=login_input).first()
        if not user_obj:
            user_obj = User.objects.filter(username__iexact=login_input).first()

        target_username = user_obj.username if user_obj else login_input
        user = authenticate(request, username=target_username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                tokens = generate_jwt_tokens(user)
                request.session['jwt_access_token'] = tokens['access_token']
                messages.success(request, f"¡Bienvenido de vuelta, {user.username}!")
                next_url = request.GET.get('next') or request.POST.get('next') or 'accounts:dashboard'
                return redirect(next_url)
            else:
                messages.error(request, "Esta cuenta ha sido desactivada.")
        else:
            messages.error(request, "Usuario/correo o contraseña inválidos.")

        form = AuthenticationForm(initial={'username': login_input})
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

    # Use single queries with only necessary fields - no conflicting select_related on self relation
    user_reviews = request.user.reviews.only(
        'id', 'user_id', 'item_type', 'item_id', 'item_title', 'rating', 'headline', 'opinion', 'created_at'
    ).order_by('-created_at')[:10]
    
    user_novels = []
    if profile.is_author:
        user_novels = request.user.novels.only(
            'id', 'slug', 'title', 'cover_image', 'cover_url', 'status', 'views_count', 'created_at'
        ).order_by('-created_at')

    context = {
        'form': form,
        'profile': profile,
        'active_tab': 'profile',
        'user_reviews': user_reviews,
        'user_novels': user_novels,
        'jwt_tokens': generate_jwt_tokens(request.user),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_view(request):
    profile = request.user.profile
    
    reviews_count = request.user.reviews.count()
    discussions_count = request.user.discussions.count()
    bookmarks_count = request.user.bookmarks.count()

    recent_reviews = request.user.reviews.only(
        'id', 'user_id', 'item_type', 'item_id', 'item_title', 'item_image', 'rating', 'headline', 'opinion', 'created_at'
    ).order_by('-created_at')[:5]

    recent_discussions = request.user.discussions.select_related('parent').only(
        'id', 'user_id', 'item_type', 'item_id', 'item_title', 'discussion_type', 'content', 'created_at', 'parent_id'
    ).order_by('-created_at')[:5]

    recent_bookmarks = request.user.bookmarks.only(
        'id', 'user_id', 'item_type', 'item_id', 'item_title', 'item_image', 'status', 'created_at'
    ).order_by('-created_at')[:6]

    author_stats = {}
    user_novels = []
    if profile.is_author:
        from novels.models import Novel, Chapter
        user_novels = Novel.objects.filter(author=request.user).prefetch_related('chapters').order_by('-created_at')[:5]
        total_novels = request.user.novels.count()
        total_views = sum(n.views_count for n in request.user.novels.only('views_count'))
        total_chapters = Chapter.objects.filter(novel__author=request.user).count()
        author_stats = {
            'total_novels': total_novels,
            'total_views': total_views,
            'total_chapters': total_chapters,
        }

    context = {
        'profile': profile,
        'active_tab': 'dashboard',
        'reviews_count': reviews_count,
        'discussions_count': discussions_count,
        'bookmarks_count': bookmarks_count,
        'recent_reviews': recent_reviews,
        'recent_discussions': recent_discussions,
        'recent_bookmarks': recent_bookmarks,
        'user_novels': user_novels,
        'author_stats': author_stats,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def dashboard_reviews_view(request):
    from django.db.models import Avg
    from novels.models import Novel
    from catalog.models import ItemReview

    profile = request.user.profile
    is_author = profile.is_author

    # Reviews written by the user across the community
    my_reviews = request.user.reviews.only(
        'id', 'user_id', 'item_type', 'item_id', 'item_title', 'item_image', 'rating', 'headline', 'opinion', 'created_at'
    ).order_by('-created_at')

    my_total_reviews = my_reviews.count()
    my_avg_rating = my_reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0

    # Rating distribution given by the user
    rating_distribution = {
        5: my_reviews.filter(rating=5).count(),
        4: my_reviews.filter(rating=4).count(),
        3: my_reviews.filter(rating=3).count(),
        2: my_reviews.filter(rating=2).count(),
        1: my_reviews.filter(rating=1).count(),
    }

    # Author specific metrics: reviews and ratings received on their own novels
    author_novels = []
    received_reviews = []
    author_received_count = 0
    author_received_avg = 0.0

    if is_author:
        author_novels = list(Novel.objects.filter(author=request.user).only('id', 'slug', 'title', 'cover_image', 'cover_url'))
        author_novel_slugs = [n.slug for n in author_novels]
        if author_novel_slugs:
            received_reviews = list(ItemReview.objects.filter(
                item_type='original_novel',
                item_id__in=author_novel_slugs
            ).select_related('user', 'user__profile').only(
                'id', 'user_id', 'item_type', 'item_id', 'item_title', 'rating', 'headline', 'opinion', 'created_at',
                'user__username', 'user__first_name', 'user__last_name', 'user__profile__role', 'user__profile__avatar_url'
            ).order_by('-created_at'))

            author_received_count = len(received_reviews)
            if author_received_count > 0:
                author_received_avg = sum(r.rating for r in received_reviews) / author_received_count

            # Attach per-novel metrics
            for n in author_novels:
                nov_revs = [r for r in received_reviews if r.item_id == n.slug]
                n.reviews_count = len(nov_revs)
                n.avg_rating = round(sum(r.rating for r in nov_revs) / len(nov_revs), 1) if nov_revs else 0.0

    context = {
        'profile': profile,
        'active_tab': 'reviews',
        'is_author': is_author,
        # Backward compatibility for existing tests
        'reviews': my_reviews,
        'total_reviews': my_total_reviews,
        'avg_rating': round(my_avg_rating, 1),
        # Enhanced role-based datasets
        'my_reviews': my_reviews,
        'my_total_reviews': my_total_reviews,
        'my_avg_rating': round(my_avg_rating, 1),
        'rating_distribution': rating_distribution,
        'author_novels': author_novels,
        'received_reviews': received_reviews,
        'author_received_count': author_received_count,
        'author_received_avg': round(author_received_avg, 1),
    }
    return render(request, 'accounts/dashboard_reviews.html', context)


@login_required
def dashboard_discussions_view(request):
    from novels.models import Novel
    from catalog.models import ItemDiscussion

    profile = request.user.profile
    is_author = profile.is_author

    # Discussions started or replied by the user
    my_discussions = list(request.user.discussions.select_related('parent').prefetch_related('replies').only(
        'id', 'user_id', 'item_type', 'item_id', 'item_title', 'discussion_type', 'content', 'created_at', 'parent_id'
    ).order_by('-created_at'))

    my_questions = [d for d in my_discussions if d.discussion_type == 'question' and d.parent_id is None]
    my_comments = [d for d in my_discussions if d.discussion_type == 'comment' or d.parent_id is not None]

    my_total_discussions = len(my_discussions)
    my_questions_count = len(my_questions)
    my_comments_count = len(my_comments)

    # Breakdown by medium for readers and authors
    breakdown_by_type = {
        'anime': sum(1 for d in my_discussions if d.item_type == 'anime'),
        'manga': sum(1 for d in my_discussions if d.item_type == 'manga'),
        'lightnovel': sum(1 for d in my_discussions if d.item_type == 'lightnovel'),
        'original_novel': sum(1 for d in my_discussions if d.item_type == 'original_novel'),
    }

    # Author specific: questions and debates raised by readers on author's works
    author_novels = []
    received_discussions = []
    received_questions_count = 0
    received_comments_count = 0

    if is_author:
        author_novels = list(Novel.objects.filter(author=request.user).only('id', 'slug', 'title'))
        author_novel_slugs = [n.slug for n in author_novels]
        if author_novel_slugs:
            received_discussions = list(ItemDiscussion.objects.filter(
                item_type='original_novel',
                item_id__in=author_novel_slugs
            ).exclude(user=request.user).select_related('user', 'user__profile', 'parent').prefetch_related('replies').only(
                'id', 'user_id', 'item_type', 'item_id', 'item_title', 'discussion_type', 'content', 'created_at', 'parent_id',
                'user__username', 'user__first_name', 'user__last_name', 'user__profile__role', 'user__profile__avatar_url'
            ).order_by('-created_at'))

            received_questions_count = sum(1 for d in received_discussions if d.discussion_type == 'question')
            received_comments_count = sum(1 for d in received_discussions if d.discussion_type == 'comment')

    context = {
        'profile': profile,
        'active_tab': 'discussions',
        'is_author': is_author,
        # Backward compatibility
        'discussions': my_discussions,
        'total_discussions': my_total_discussions,
        'questions_count': my_questions_count,
        'comments_count': my_comments_count,
        # Enhanced role-based datasets
        'my_discussions': my_discussions,
        'my_questions': my_questions,
        'my_comments': my_comments,
        'my_total_discussions': my_total_discussions,
        'my_questions_count': my_questions_count,
        'my_comments_count': my_comments_count,
        'breakdown_by_type': breakdown_by_type,
        'author_novels': author_novels,
        'received_discussions': received_discussions,
        'received_total_discussions': len(received_discussions),
        'received_questions_count': received_questions_count,
        'received_comments_count': received_comments_count,
    }
    return render(request, 'accounts/dashboard_discussions.html', context)


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

