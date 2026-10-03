from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.views.decorators.http import require_GET
from novels.models import Novel
from catalog.models import ItemDiscussion


@require_GET
def api_novels_optimized_view(request):
    """
    Optimized endpoint returning community novels with 1 single query
    and strictly fetching only necessary fields (avoiding heavy text fields).
    """
    page_num = int(request.GET.get('page', 1) or 1)
    per_page = int(request.GET.get('per_page', 24) or 24)
    q = request.GET.get('q', '').strip()

    # Single consolidated query with select_related and only necessary fields
    queryset = Novel.objects.exclude(status='draft').select_related(
        'author', 'author__profile'
    ).prefetch_related('categories').only(
        'id', 'slug', 'title', 'cover_image', 'cover_url',
        'status', 'views_count', 'created_at',
        'author__username', 'author__profile__uid'
    )

    if q:
        queryset = queryset.filter(title__icontains=q)

    queryset = queryset.order_by('-created_at')

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page_num)

    results = []
    for n in page_obj:
        author_profile = getattr(n.author, 'profile', None)
        author_uid = str(author_profile.uid) if author_profile and author_profile.uid else ''
        results.append({
            'slug': n.slug,
            'title': n.title,
            'cover': n.final_cover,
            'status': n.get_status_display(),
            'views_count': n.views_count,
            'author': {
                'username': n.author.username,
                'uid': author_uid,
            },
            'categories': [c.name for c in n.categories.all()],
        })

    return JsonResponse({
        'status': 'success',
        'total': paginator.count,
        'page': page_obj.number,
        'total_pages': paginator.num_pages,
        'items': results
    })


@require_GET
def api_live_metrics_view(request):
    """
    Single consolidated query for real-time live platform metrics.
    """
    novel_stats = Novel.objects.exclude(status='draft').aggregate(
        total_novels=Count('id'),
        total_views=Sum('views_count')
    )

    latest_discussions = list(
        ItemDiscussion.objects.filter(parent__isnull=True)
        .select_related('user', 'user__profile')
        .only('id', 'item_title', 'content', 'created_at', 'user__username', 'user__profile__uid')
        .order_by('-created_at')[:3]
        .values('id', 'item_title', 'content', 'created_at', 'user__username', 'user__profile__uid')
    )

    for d in latest_discussions:
        d['uid'] = str(d.pop('user__profile__uid', ''))
        d['username'] = d.pop('user__username', 'anon')
        d['created_at'] = d['created_at'].isoformat() if d.get('created_at') else ''

    return JsonResponse({
        'status': 'success',
        'metrics': {
            'total_novels': novel_stats.get('total_novels') or 0,
            'total_views': novel_stats.get('total_views') or 0,
            'latest_discussions': latest_discussions,
        }
    })


@require_GET
def api_live_notifications_view(request):
    """
    Single consolidated query endpoint for notifications, returning role-differentiated
    notifications (reviews/ratings and questions/discussions) with minimal fields.
    """
    from catalog.models import ItemReview, ItemDiscussion

    notifications = []

    latest_review = ItemReview.objects.select_related('user').only(
        'id', 'item_title', 'rating', 'headline', 'user__username'
    ).order_by('-created_at').first()

    if latest_review:
        notifications.append({
            'type': 'review',
            'icon': 'bi-star-fill text-warning',
            'title': 'Nueva Calificación / Reseña',
            'text': f"@{latest_review.user.username} calificó '{latest_review.item_title}' con {latest_review.rating} estrellas: \"{latest_review.headline}\"",
            'duration': 5000,
        })

    latest_discussion = ItemDiscussion.objects.select_related('user').only(
        'id', 'item_title', 'discussion_type', 'content', 'user__username'
    ).order_by('-created_at').first()

    if latest_discussion:
        disc_type = 'Pregunta' if latest_discussion.discussion_type == 'question' else 'Debate'
        notifications.append({
            'type': 'discussion',
            'icon': 'bi-chat-left-dots-fill text-info',
            'title': f'Nueva Participación ({disc_type})',
            'text': f"@{latest_discussion.user.username} en '{latest_discussion.item_title}': \"{latest_discussion.content[:65]}...\"",
            'duration': 5000,
        })

    return JsonResponse({
        'status': 'success',
        'notifications': notifications
    })


@require_GET
def ws_live_http_fallback_view(request):
    """
    HTTP fallback view for /ws/live/ to prevent 404 errors when accessed via HTTP/WSGI.
    Provides live status and prevents unnecessary error logging in production.
    """
    return JsonResponse({
        'status': 'active',
        'endpoint': '/ws/live/',
        'protocol': 'websocket',
        'message': 'ASGI WebSocket gateway ready'
    })


# ==============================================================================
# TENRAI API GATEWAY & ENDPOINT CONSUMPTION
# ==============================================================================

@require_GET
def api_tenrai_proxy_view(request, path):
    """
    Direct proxy gateway to Tenrai API allowing frontend and clients to query
    any of the 94 GET endpoints documented in OpenAPI 3.0 specification.
    Example: /api/tenrai/anime/1/videos, /api/tenrai/top/anime, /api/tenrai/seasons/now
    """
    from catalog.services import tenrai_service
    params = request.GET.dict()
    data = tenrai_service.request_endpoint(path, params=params)
    if data is not None:
        return JsonResponse(data, safe=False)
    return JsonResponse({'status': 'error', 'message': f'Recurso no encontrado o no disponible en Tenrai API: /{path}'}, status=404)


@require_GET
def api_tenrai_item_extra_view(request, media_type, item_id, extra):
    """
    Fetches rich sub-resource metadata for anime or manga (episodes, videos, characters, staff, reviews, etc.).
    """
    from catalog.services import tenrai_service
    endpoint_path = f"/{media_type}/{item_id}/{extra}"
    params = request.GET.dict()
    data = tenrai_service.request_endpoint(endpoint_path, params=params)
    if data is not None:
        return JsonResponse(data, safe=False)
    return JsonResponse({'status': 'error', 'message': f'Metadato no encontrado en Tenrai API: {endpoint_path}'}, status=404)


@require_GET
def api_tenrai_random_view(request, media_type='anime'):
    """Returns random anime, manga, character, or person from Tenrai API."""
    from catalog.services import tenrai_service
    endpoint = f"/random/{media_type}"
    data = tenrai_service.request_endpoint(endpoint)
    if data is not None:
        return JsonResponse(data, safe=False)
    return JsonResponse({'status': 'error', 'message': f'No se pudo obtener recurso aleatorio de {media_type}'}, status=502)


@require_GET
def api_tenrai_seasons_view(request):
    """Returns current or upcoming seasonal anime from Tenrai API."""
    from catalog.services import tenrai_service
    sub = request.GET.get('sub', 'now')  # now, upcoming, or empty for all seasons
    endpoint = f"/seasons/{sub}" if sub in ('now', 'upcoming') else '/seasons'
    data = tenrai_service.request_endpoint(endpoint, params=request.GET.dict())
    if data is not None:
        return JsonResponse(data, safe=False)
    return JsonResponse({'status': 'error', 'message': 'No se pudo obtener la temporada actual'}, status=502)


@require_GET
def api_tenrai_schedules_view(request):
    """Returns anime airing schedules from Tenrai API."""
    from catalog.services import tenrai_service
    data = tenrai_service.request_endpoint('/schedules', params=request.GET.dict())
    if data is not None:
        return JsonResponse(data, safe=False)
    return JsonResponse({'status': 'error', 'message': 'No se pudo obtener la programación semanal'}, status=502)


@require_GET
def api_tenrai_news_view(request):
    """Returns news from Tenrai API."""
    from catalog.services import tenrai_service
    data = tenrai_service.request_endpoint('/news', params=request.GET.dict())
    if data is not None:
        return JsonResponse(data, safe=False)
    return JsonResponse({'status': 'error', 'message': 'No se pudo obtener noticias'}, status=502)


@require_GET
def api_tenrai_articles_view(request):
    """Returns featured articles from Tenrai API."""
    from catalog.services import tenrai_service
    data = tenrai_service.request_endpoint('/articles', params=request.GET.dict())
    if data is not None:
        return JsonResponse(data, safe=False)
    return JsonResponse({'status': 'error', 'message': 'No se pudo obtener artículos'}, status=502)


@require_GET
def api_tenrai_stacks_view(request):
    """Returns interest stacks from Tenrai API."""
    from catalog.services import tenrai_service
    data = tenrai_service.request_endpoint('/stacks', params=request.GET.dict())
    if data is not None:
        return JsonResponse(data, safe=False)
    return JsonResponse({'status': 'error', 'message': 'No se pudo obtener interest stacks'}, status=502)

