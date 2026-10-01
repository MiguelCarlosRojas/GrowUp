from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Novel, Chapter, Category
from .forms import NovelForm, ChapterForm
from catalog.models import ItemReview, ItemDiscussion


def novel_list(request):
    novels = Novel.objects.exclude(status='draft').select_related('author').prefetch_related('categories')

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

    categories = Category.objects.all()

    context = {
        'novels': novels,
        'categories': categories,
        'selected_q': q,
        'selected_category': category_slug,
        'selected_status': status,
        'selected_order': order,
    }
    return render(request, 'novels/novel_list.html', context)


def novel_detail(request, slug):
    novel = get_object_or_404(Novel.objects.select_related('author').prefetch_related('categories'), slug=slug)
    
    # Increment views
    Novel.objects.filter(pk=novel.pk).update(views_count=novel.views_count + 1)
    novel.views_count += 1

    chapters = novel.published_chapters()
    if request.user == novel.author or request.user.is_staff:
        chapters = novel.chapters.all().order_by('chapter_number')

    reviews = ItemReview.objects.filter(item_type='original_novel', item_id=novel.slug).select_related('user')
    discussions = ItemDiscussion.objects.filter(item_type='original_novel', item_id=novel.slug, parent__isnull=True).select_related('user').prefetch_related('replies__user')

    context = {
        'novel': novel,
        'chapters': chapters,
        'reviews': reviews,
        'discussions': discussions,
    }
    return render(request, 'novels/novel_detail.html', context)


def chapter_read(request, novel_slug, chapter_number):
    novel = get_object_or_404(Novel, slug=novel_slug)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)

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
    return render(request, 'novels/author_dashboard.html', {'novels': novels})


@login_required
def novel_create(request):
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES)
        if form.is_valid():
            novel = form.save(commit=False)
            novel.author = request.user
            novel.save()
            form.save_m2m()
            messages.success(request, f"¡Novela '{novel.title}' creada con éxito!")
            return redirect('novels:author_dashboard')
    else:
        form = NovelForm()

    return render(request, 'novels/novel_form.html', {'form': form, 'title': 'Publicar Nueva Novela Ligera'})


@login_required
def novel_edit(request, slug):
    novel = get_object_or_404(Novel, slug=slug, author=request.user)
    if request.method == 'POST':
        form = NovelForm(request.POST, request.FILES, instance=novel)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡Novela '{novel.title}' actualizada!")
            return redirect('novels:author_dashboard')
    else:
        form = NovelForm(instance=novel)

    return render(request, 'novels/novel_form.html', {'form': form, 'title': f'Editar Novela: {novel.title}', 'novel': novel})


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
            messages.success(request, f"¡Capítulo {chapter.chapter_number} publicado con éxito!")
            return redirect('novels:novel_detail', slug=novel.slug)
    else:
        form = ChapterForm(initial={'chapter_number': next_num, 'is_published': True})

    return render(request, 'novels/chapter_form.html', {'form': form, 'novel': novel, 'title': f'Añadir Capítulo a {novel.title}'})


@login_required
def chapter_edit(request, novel_slug, chapter_number):
    novel = get_object_or_404(Novel, slug=novel_slug, author=request.user)
    chapter = get_object_or_404(Chapter, novel=novel, chapter_number=chapter_number)

    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡Capítulo {chapter.chapter_number} actualizado con éxito!")
            return redirect('novels:novel_detail', slug=novel.slug)
    else:
        form = ChapterForm(instance=chapter)

    return render(request, 'novels/chapter_form.html', {'form': form, 'novel': novel, 'title': f'Editar Capítulo {chapter.chapter_number}'})
