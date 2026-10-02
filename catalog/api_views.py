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
