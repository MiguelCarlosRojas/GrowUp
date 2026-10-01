from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .services import jikan_service
from .models import ItemReview, ItemDiscussion, Bookmark
from .forms import ReviewForm, DiscussionForm
from novels.models import Novel, Category


def home_view(request):
    # Fetch real data from Jikan API
    top_animes = jikan_service.get_top_anime(limit=8)
    top_mangas = jikan_service.get_top_manga(limit=8)
    top_lightnovels = jikan_service.get_top_lightnovels(limit=8)

    # Community original light novels from local database
    original_novels = Novel.objects.exclude(status='draft').order_by('-views_count')[:6]

    # Quick stats
    hero_item = top_animes[0] if top_animes else None

    context = {
        'hero_item': hero_item,
        'top_animes': top_animes,
        'top_mangas': top_mangas,
        'top_lightnovels': top_lightnovels,
        'original_novels': original_novels,
        'genres': jikan_service.get_common_genres(),
    }
    return render(request, 'catalog/home.html', context)


def explore_view(request):
    media_type = request.GET.get('type', 'anime')  # anime, manga, lightnovel, original_novel
    q = request.GET.get('q', '').strip()
    genre = request.GET.get('genre', '').strip()
    status = request.GET.get('status', '').strip()
    order_by = request.GET.get('order_by', 'score').strip()
    sort = request.GET.get('sort', 'desc').strip()

    if media_type == 'original_novel':
        novels = Novel.objects.exclude(status='draft')
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

        items = []
        for n in novels:
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
    else:
        results = jikan_service.search_items(
            category=media_type,
            query=q,
            genre=genre,
            status=status,
            order_by=order_by,
            sort=sort
        )
        items = results.get('items', [])

    context = {
        'items': items,
        'selected_type': media_type,
        'selected_q': q,
        'selected_genre': genre,
        'selected_status': status,
        'selected_order_by': order_by,
        'selected_sort': sort,
        'genres': jikan_service.get_common_genres(),
        'novel_categories': Category.objects.all(),
    }
    return render(request, 'catalog/explore.html', context)


def item_detail_view(request, item_type, item_id):
    # Fetch real item details from Jikan API
    item = jikan_service.get_item_detail(item_type, item_id)
    if not item:
        messages.error(request, "No se pudo obtener la información de esta obra.")
        return redirect('catalog:explore')

    # Fetch ratings, reviews, discussions from database
    reviews = ItemReview.objects.filter(item_type=item_type, item_id=str(item_id)).select_related('user')
    stats = reviews.aggregate(avg_score=Avg('rating'), count=Count('id'))

    discussions = ItemDiscussion.objects.filter(
        item_type=item_type,
        item_id=str(item_id),
        parent__isnull=True
    ).select_related('user').prefetch_related('replies__user')

    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, item_type=item_type, item_id=str(item_id)).exists()

    review_form = ReviewForm()
    discussion_form = DiscussionForm()

    context = {
        'item': item,
        'item_type': item_type,
        'item_id': item_id,
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
