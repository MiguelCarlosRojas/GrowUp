from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import ContactMessage, BlogPost, BlogComment
from .forms import ContactForm, BlogPostForm, BlogCommentForm


def user_can_manage_blog(user):
    """
    Ensures only authorized platform administrator / superuser can publish, edit or delete blog articles.
    Regular logged-in users have permission to read, share, and post comments on blog articles.
    """
    if not user or not user.is_authenticated:
        return False
    return user.is_superuser or user.username in ['Anmigz', 'admin']


# ==============================================================================
# Sobre Nosotros
# ==============================================================================

def quienes_somos_view(request):
    return render(request, 'pages/quienes_somos.html')


def nuestra_historia_view(request):
    return render(request, 'pages/nuestra_historia.html')


def donde_estamos_view(request):
    return render(request, 'pages/donde_estamos.html')


# ==============================================================================
# Blog Oficial GrowUp (Lectura global, compartir, gestión exclusiva de autor)
# ==============================================================================

def blog_view(request):
    category = request.GET.get('category', '').strip()
    query = request.GET.get('q', '').strip()

    posts_qs = BlogPost.objects.filter(is_published=True).select_related('author', 'author__profile')

    if category:
        posts_qs = posts_qs.filter(category__iexact=category)
    if query:
        posts_qs = posts_qs.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query)
        )

    posts_qs = posts_qs.order_by('-created_at')

    paginator = Paginator(posts_qs, 6)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        posts = paginator.page(1)

    categories = BlogPost.objects.filter(is_published=True).values_list('category', flat=True).distinct()
    can_manage = user_can_manage_blog(request.user)

    return render(request, 'pages/blog.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': category,
        'query': query,
        'can_manage': can_manage,
    })


def blog_detail_view(request, slug):
    post = get_object_or_404(BlogPost.objects.select_related('author', 'author__profile'), slug=slug)

    can_manage = user_can_manage_blog(request.user)
    if not post.is_published and not can_manage:
        messages.error(request, "Este artículo se encuentra en revisión o no está disponible públicamente.")
        return redirect('catalog:blog')

    # Increment view count
    BlogPost.objects.filter(pk=post.pk).update(views_count=post.views_count + 1)
    post.views_count += 1

    comments = post.comments.select_related('user', 'user__profile').order_by('created_at')
    comment_form = BlogCommentForm()

    related_posts = BlogPost.objects.filter(
        is_published=True, category=post.category
    ).exclude(pk=post.pk).order_by('-created_at')[:3]

    current_url = request.build_absolute_uri()

    return render(request, 'pages/blog_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
        'can_manage': can_manage,
        'current_url': current_url,
    })


@login_required
def blog_add_comment_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Tu comentario ha sido publicado en el artículo.")
        else:
            messages.error(request, "El comentario no puede estar vacío.")
    return redirect('catalog:blog_detail', slug=slug)


@login_required
def blog_create_view(request):
    if not user_can_manage_blog(request.user):
        messages.error(request, "Acceso restringido: Solo el autor y administrador pueden redactar artículos.")
        return redirect('catalog:blog')

    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f"¡El artículo '{post.title}' ha sido publicado exitosamente!")
            return redirect('catalog:blog_detail', slug=post.slug)
    else:
        form = BlogPostForm()

    return render(request, 'pages/blog_form.html', {
        'form': form,
        'action_title': 'Nuevo Artículo del Blog',
        'button_text': 'Publicar Artículo',
    })


@login_required
def blog_edit_view(request, slug):
    if not user_can_manage_blog(request.user):
        messages.error(request, "Acceso restringido: No cuentas con permisos de edición para este artículo.")
        return redirect('catalog:blog')

    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡El artículo '{post.title}' se ha actualizado correctamente!")
            return redirect('catalog:blog_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'pages/blog_form.html', {
        'form': form,
        'post': post,
        'action_title': f"Editar: {post.title}",
        'button_text': 'Guardar Cambios',
    })


@login_required
def blog_delete_view(request, slug):
    if not user_can_manage_blog(request.user):
        messages.error(request, "Acceso restringido: No cuentas con permisos para eliminar artículos.")
        return redirect('catalog:blog')

    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f"El artículo '{title}' ha sido eliminado.")
        return redirect('catalog:blog')

    return render(request, 'pages/blog_confirm_delete.html', {'post': post})


# ==============================================================================
# Ayuda & Contacto (Persistencia completa en Prisma Postgres)
# ==============================================================================

def ayuda_view(request):
    return render(request, 'pages/ayuda.html')


def preguntas_frecuentes_view(request):
    return render(request, 'pages/preguntas_frecuentes.html')


def contacto_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['name']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['subject']
            mensaje = form.cleaned_data['message']

            if request.user.is_authenticated:
                # If user already has an active pending ticket, update it; otherwise create a new one
                existing_ticket = ContactMessage.objects.filter(
                    user=request.user, status='pending'
                ).order_by('-created_at').first()

                if existing_ticket:
                    existing_ticket.name = nombre
                    existing_ticket.email = email
                    existing_ticket.subject = asunto
                    existing_ticket.message = mensaje
                    existing_ticket.save()
                    messages.success(request, f"¡Tu solicitud de soporte ha sido actualizada exitosamente, {nombre}! Nuestro equipo te responderá a {email}.")
                else:
                    ticket = form.save(commit=False)
                    ticket.user = request.user
                    ticket.save()
                    messages.success(request, f"¡Gracias por comunicarte con nosotros, {nombre}! Tu solicitud ha sido registrada en el sistema de soporte.")
            else:
                form.save()
                messages.success(request, f"¡Gracias por comunicarte con nosotros, {nombre}! Tu mensaje ha sido registrado exitosamente en nuestro sistema.")
            return redirect('catalog:contacto')
        else:
            messages.error(request, "Por favor verifica los campos obligatorios del formulario de contacto.")
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['name'] = request.user.get_full_name() or request.user.username
            initial_data['email'] = request.user.email
        form = ContactForm(initial=initial_data)

    user_tickets = []
    if request.user.is_authenticated:
        user_tickets = ContactMessage.objects.filter(user=request.user).order_by('-created_at')[:5]

    return render(request, 'pages/contacto.html', {
        'form': form,
        'user_tickets': user_tickets,
    })


# ==============================================================================
# Legal & Políticas
# ==============================================================================

def aviso_legal_view(request):
    return render(request, 'pages/aviso_legal.html')


def politica_cookies_view(request):
    return render(request, 'pages/politica_cookies.html')


def condiciones_uso_view(request):
    return render(request, 'pages/condiciones_uso.html')


def politica_privacidad_view(request):
    return render(request, 'pages/politica_privacidad.html')


def declaracion_accesibilidad_view(request):
    return render(request, 'pages/declaracion_accesibilidad.html')

