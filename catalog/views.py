from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .services import tenrai_service
from .models import ItemReview, ItemDiscussion, Bookmark
from .forms import ReviewForm, DiscussionForm
from novels.models import Novel, Category


def home_view(request):
    # Only local DB query - NO external API calls for instant page load
    original_novels = Novel.objects.exclude(status='draft').select_related(
        'author', 'author__profile'
    ).only(
        'id', 'slug', 'title', 'cover_image', 'cover_url', 'synopsis', 'views_count',
        'author__username', 'author__profile__uid'
    ).order_by('-views_count')[:6]

    context = {
        'original_novels': original_novels,
        'genres': tenrai_service.get_common_genres(),
    }
    return render(request, 'catalog/home.html', context)


def explore_view(request):
    media_type = request.GET.get('type', 'anime')  # anime, manga, lightnovel, original_novel, characters, people
    q = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '').strip()
    status = request.GET.get('status', '').strip()
    order_by = request.GET.get('order_by', 'score').strip()
    sort = request.GET.get('sort', 'desc').strip()
    format_type = request.GET.get('format', '').strip()
    rating = request.GET.get('rating', '').strip()
    min_score = request.GET.get('min_score', '').strip()

    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    per_page = 24

    if media_type == 'original_novel':
        novels = Novel.objects.exclude(status='draft').select_related(
            'author', 'author__profile'
        ).prefetch_related('categories').only(
            'id', 'slug', 'title', 'cover_image', 'cover_url', 'status', 'synopsis', 'views_count', 'created_at',
            'author__username', 'author__profile__uid'
        )
        if q:
            novels = novels.filter(title__icontains=q)
        if genre:
            novels = novels.filter(categories__slug=genre)
        if status:
            novels = novels.filter(status=status)
        if order_by == 'title':
            novels = novels.order_by('title')
        elif order_by == 'popularity':
            novels = novels.order_by('-views_count')
        else:
            novels = novels.order_by('-created_at')

        paginator = Paginator(novels, per_page)
        try:
            novels_page = paginator.page(page)
        except (EmptyPage, PageNotAnInteger):
            novels_page = paginator.page(1)
            page = 1

        items = []
        for n in novels_page:
            items.append({
                'mal_id': n.slug,
                'is_original': True,
                'title': n.title,
                'images': {'jpg': {'large_image_url': n.final_cover}},
                'score': 'Comunidad',
                'type': 'Novela Original',
                'synopsis': n.synopsis,
                'genres': [{'name': c.name} for c in n.categories.all()],
                'status': n.get_status_display(),
            })

        page_range = tenrai_service.get_sliding_page_range(novels_page.number, paginator.num_pages, window_size=5)

        pagination = {
            'current_page': novels_page.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'per_page': per_page,
            'has_previous_page': novels_page.has_previous(),
            'has_next_page': novels_page.has_next(),
            'previous_page_number': novels_page.previous_page_number() if novels_page.has_previous() else None,
            'next_page_number': novels_page.next_page_number() if novels_page.has_next() else None,
            'page_range': page_range,
            'start_index': novels_page.start_index() if paginator.count > 0 else 0,
            'end_index': novels_page.end_index() if paginator.count > 0 else 0,
        }
    else:
        results = tenrai_service.search_items(
            category=media_type,
            query=q,
            genre=genre,
            status=status,
            order_by=order_by,
            sort=sort,
            page=page,
            per_page=per_page,
            format_type=format_type,
            rating=rating,
            min_score=min_score,
        )
        items = results.get('items', [])
        pagination = results.get('pagination', {
            'current_page': 1,
            'total_pages': 1,
            'total_items': len(items),
            'per_page': per_page,
            'has_previous_page': False,
            'has_next_page': False,
            'previous_page_number': None,
            'next_page_number': None,
            'page_range': [1],
            'start_index': 1 if items else 0,
            'end_index': len(items),
        })

    context = {
        'items': items,
        'pagination': pagination,
        'selected_type': media_type,
        'selected_q': q,
        'selected_genre': genre,
        'selected_status': status,
        'selected_order_by': order_by,
        'selected_sort': sort,
        'selected_format': format_type,
        'selected_rating': rating,
        'selected_min_score': min_score,
        'genres': tenrai_service.get_common_genres(),
        'novel_categories': Category.objects.all(),
    }
    return render(request, 'catalog/explore.html', context)


def item_detail_view(request, item_type, item_id):
    # Fetch real item details from Tenrai API
    item = tenrai_service.get_item_detail(item_type, item_id)
    if not item:
        messages.error(request, "No se pudo obtener la información de esta obra.")
        return redirect('catalog:explore')

    # Fetch ratings, reviews, discussions from database with single queries and only needed fields
    reviews = ItemReview.objects.filter(item_type=item_type, item_id=str(item_id)).select_related(
        'user', 'user__profile'
    ).only('id', 'item_type', 'item_id', 'rating', 'headline', 'opinion', 'created_at', 'user__username', 'user__profile__uid')
    stats = reviews.aggregate(avg_score=Avg('rating'), count=Count('id'))

    discussions = ItemDiscussion.objects.filter(
        item_type=item_type,
        item_id=str(item_id),
        parent__isnull=True
    ).select_related('user', 'user__profile').prefetch_related('replies__user', 'replies__user__profile').only(
        'id', 'item_type', 'item_id', 'discussion_type', 'content', 'created_at', 'parent_id', 'user__username', 'user__profile__uid'
    )

    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, item_type=item_type, item_id=str(item_id)).exists()

    # Platforms (Official and Community / Streaming & Reading)
    platforms = tenrai_service.get_platforms_fast(item_type, item.get('title') or item.get('name') or '', item_id)
    share_url = request.build_absolute_uri()
    share_title = item.get('title') or item.get('name') or 'GrowUp'

    review_form = ReviewForm()
    discussion_form = DiscussionForm()

    context = {
        'item': item,
        'item_type': item_type,
        'item_id': item_id,
        'platforms': platforms,
        'share_url': share_url,
        'share_title': share_title,
        'reviews': reviews,
        'avg_score': stats.get('avg_score'),
        'total_reviews': stats.get('count', 0),
        'discussions': discussions,
        'is_bookmarked': is_bookmarked,
        'review_form': review_form,
        'discussion_form': discussion_form,
    }
    return render(request, 'catalog/item_detail.html', context)


@login_required
def add_review_view(request, item_type, item_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            item_title = request.POST.get('item_title', 'Obra')
            item_image = request.POST.get('item_image', '')
            
            review, created = ItemReview.objects.update_or_create(
                user=request.user,
                item_type=item_type,
                item_id=str(item_id),
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'headline': form.cleaned_data['headline'],
                    'opinion': form.cleaned_data['opinion'],
                    'item_title': item_title,
                    'item_image': item_image,
                }
            )
            msg = "¡Tu opinión y clasificación han sido publicadas con éxito!" if created else "¡Tu reseña ha sido actualizada!"
            messages.success(request, msg)
        else:
            messages.error(request, "Por favor completa correctamente los campos de la opinión.")

    if item_type == 'original_novel':
        return redirect('novels:novel_detail', slug=item_id)
    return redirect('catalog:item_detail', item_type=item_type, item_id=item_id)


@login_required
def add_discussion_view(request, item_type, item_id):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent = None
            if parent_id:
                parent = ItemDiscussion.objects.filter(id=parent_id).first()

            discussion = form.save(commit=False)
            discussion.user = request.user
            discussion.item_type = item_type
            discussion.item_id = str(item_id)
            discussion.item_title = request.POST.get('item_title', '')
            discussion.parent = parent
            discussion.save()
            
            msg = "Tu respuesta ha sido enviada." if parent else "Tu comentario o pregunta ha sido publicado."
            messages.success(request, msg)
        else:
            messages.error(request, "El mensaje no puede estar vacío.")

    if item_type == 'original_novel':
        return redirect('novels:novel_detail', slug=item_id)
    return redirect('catalog:item_detail', item_type=item_type, item_id=item_id)


@login_required
def toggle_bookmark_view(request, item_type, item_id):
    bookmark = Bookmark.objects.filter(user=request.user, item_type=item_type, item_id=str(item_id)).first()
    if bookmark:
        bookmark.delete()
        messages.info(request, "Removido de tus favoritos.")
    else:
        title = request.POST.get('item_title', 'Obra')
        image = request.POST.get('item_image', '')
        Bookmark.objects.create(
            user=request.user,
            item_type=item_type,
            item_id=str(item_id),
            item_title=title,
            item_image=image
        )
        messages.success(request, f"'{title}' ha sido añadido a tus favoritos.")

    if item_type == 'original_novel':
        return redirect('novels:novel_detail', slug=item_id)
    return redirect('catalog:item_detail', item_type=item_type, item_id=item_id)
