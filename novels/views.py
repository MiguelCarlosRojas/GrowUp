from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Novel, Chapter, Category
from .forms import NovelForm, ChapterForm
from catalog.models import ItemReview, ItemDiscussion


def novel_list(request):
    novels = Novel.objects.exclude(status='draft').select_related(
        'author', 'author__profile'
    ).prefetch_related('categories').only(
        'id', 'slug', 'title', 'cover_image', 'cover_url', 'synopsis', 'status', 'views_count', 'created_at',
        'author__username', 'author__profile__uid'
    )

    q = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()
    order = request.GET.get('order', '-created_at')

    if q:
        novels = novels.filter(Q(title__icontains=q) | Q(synopsis__icontains=q) | Q(author__username__icontains=q))
    if category_slug:
        novels = novels.filter(categories__slug=category_slug)
    if status:
        novels = novels.filter(status=status)

    valid_orders = {
        'newest': '-created_at',
        'popular': '-views_count',
        'title': 'title',
    }
    novels = novels.order_by(valid_orders.get(order, '-created_at'))

    # 24 records per page
    per_page = 24
    paginator = Paginator(novels, per_page)
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    try:
        page_obj = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)

    categories = Category.objects.all()

    context = {
        'novels': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'categories': categories,
        'selected_q': q,
        'selected_category': category_slug,
        'selected_status': status,
        'selected_order': order,
    }
    return render(request, 'novels/novel_list.html', context)


def novel_detail(request, slug):
    novel = get_object_or_404(
        Novel.objects.select_related('author', 'author__profile').prefetch_related('categories'),
        slug=slug
    )
    
    # Increment views atomically
    Novel.objects.filter(pk=novel.pk).update(views_count=novel.views_count + 1)
    novel.views_count += 1

    chapters = novel.published_chapters()
    if request.user == novel.author or request.user.is_staff:
        chapters = novel.chapters.all().order_by('chapter_number')

    reviews = ItemReview.objects.filter(item_type='original_novel', item_id=novel.slug).select_related(
        'user', 'user__profile'
    ).only('id', 'item_type', 'item_id', 'rating', 'headline', 'opinion', 'created_at', 'user__username', 'user__profile__uid')
    
    discussions = ItemDiscussion.objects.filter(
        item_type='original_novel', item_id=novel.slug, parent__isnull=True
    ).select_related('user', 'user__profile').prefetch_related('replies__user', 'replies__user__profile').only(
        'id', 'item_type', 'item_id', 'discussion_type', 'content', 'created_at', 'parent_id', 'user__username', 'user__profile__uid'
    )

    share_url = request.build_absolute_uri()
    share_title = novel.title

    context = {
        'novel': novel,
        'chapters': chapters,
        'reviews': reviews,
        'discussions': discussions,
        'share_url': share_url,
        'share_title': share_title,
    }
    return render(request, 'novels/novel_detail.html', context)


def chapter_read(request, novel_slug, chapter_number):
    novel = get_object_or_404(Novel.objects.only('id', 'slug', 'title', 'author_id'), slug=novel_slug)
    chapter = get_object_or_404(
        Chapter.objects.select_related('novel').only(
            'id', 'novel_id', 'chapter_number', 'title', 'content', 'author_notes', 'is_published', 'words_count', 'created_at', 'published_at', 'updated_at',
            'novel__id', 'novel__slug', 'novel__title', 'novel__author_id'
        ),
        novel=novel,
        chapter_number=chapter_number
    )

    if not chapter.is_published and request.user != novel.author and not request.user.is_staff:
        messages.error(request, "Este capítulo aún no ha sido publicado por el autor.")
        return redirect('novels:novel_detail', slug=novel.slug)

    next_chapter = chapter.get_next_chapter()
    prev_chapter = chapter.get_previous_chapter()

    context = {
        'novel': novel,
        'chapter': chapter,
        'next_chapter': next_chapter,
        'prev_chapter': prev_chapter,
    }
    return render(request, 'novels/chapter_read.html', context)


@login_required
def author_dashboard(request):
    # Ensure profile role is author or allow upgrading
    if request.user.profile.role != 'author':
        request.user.profile.role = 'author'
        request.user.profile.save()

    novels = Novel.objects.filter(author=request.user).prefetch_related('chapters')
    return render(request, 'novels/author_dashboard.html', {'novels': novels, 'active_tab': 'workshop'})


@login_required
def novel_create(request):
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES)
        if form.is_valid():
            novel = form.save(commit=False)
            novel.author = request.user
            novel.save()
            form.save_m2m()
            messages.success(request, f"Novela '{novel.title}' creada con éxito. Procede a redactar su primer capítulo.")
            return redirect('novels:chapter_create', novel_slug=novel.slug)
    else:
        form = NovelForm()

    return render(request, 'novels/novel_form.html', {'form': form, 'title': 'Publicar Nueva Novela Ligera', 'active_tab': 'workshop'})


@login_required
def toggle_novel_visibility(request, slug):
    novel = get_object_or_404(Novel, slug=slug, author=request.user)
    if request.method == 'POST':
        if novel.status == 'draft':
            novel.status = 'ongoing'
            messages.success(request, f"La novela '{novel.title}' ahora está Pública (En Emisión) en el catálogo.")
        else:
            novel.status = 'draft'
            messages.info(request, f"La novela '{novel.title}' ahora está en modo Privado (Borrador).")
        novel.save(update_fields=['status'])
    return redirect('novels:author_dashboard')


@login_required
def novel_edit(request, slug):
    novel = get_object_or_404(Novel, slug=slug, author=request.user)
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES, instance=novel)
        if form.is_valid():
            form.save()
            messages.success(request, f"Novela '{novel.title}' actualizada.")
            return redirect('novels:author_dashboard')
    else:
        form = NovelForm(instance=novel)

    return render(request, 'novels/novel_form.html', {'form': form, 'title': f'Editar Novela: {novel.title}', 'novel': novel, 'active_tab': 'workshop'})


@login_required
def chapter_create(request, novel_slug):
    novel = get_object_or_404(Novel, slug=novel_slug, author=request.user)
    next_num = (novel.chapters.count() + 1)
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.novel = novel
            chapter.save()
            messages.success(request, f"Capítulo {chapter.chapter_number} guardado con éxito.")
            action = request.POST.get('action')
            if action == 'add_another':
                return redirect('novels:chapter_create', novel_slug=novel.slug)
            return redirect('novels:author_dashboard')
    else:
        form = ChapterForm(initial={'chapter_number': next_num, 'is_published': True})

    return render(request, 'novels/chapter_form.html', {'form': form, 'novel': novel, 'title': f'Añadir Capítulo a {novel.title}', 'active_tab': 'workshop'})


@login_required
def chapter_edit(request, novel_slug, chapter_number):
    novel = get_object_or_404(Novel, slug=novel_slug, author=request.user)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)

    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, f"Capítulo {chapter.chapter_number} actualizado con éxito.")
            return redirect('novels:author_dashboard')
    else:
        form = ChapterForm(instance=chapter)

    return render(request, 'novels/chapter_form.html', {'form': form, 'novel': novel, 'title': f'Editar Capítulo {chapter.chapter_number}', 'active_tab': 'workshop'})

