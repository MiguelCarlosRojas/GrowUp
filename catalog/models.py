from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class ItemReview(models.Model):
    ITEM_TYPES = [
        ('anime', 'Anime'),
        ('manga', 'Manga'),
        ('lightnovel', 'Novela Ligera (MAL)'),
        ('original_novel', 'Novela Original'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    item_id = models.CharField(max_length=100, db_index=True, help_text="ID de Tenrai MAL o slug de novela")
    item_title = models.CharField(max_length=255)
    item_image = models.URLField(blank=True, max_length=500)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Clasificación de 1 a 5 estrellas"
    )
    headline = models.CharField(max_length=150, help_text="Título de la opinión")
    opinion = models.TextField(help_text="Texto detallado de la opinión o reseña")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Opinión / Reseña"
        verbose_name_plural = "Opiniones y Reseñas"
        unique_together = ['user', 'item_type', 'item_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.item_title} ({self.rating}/5)"


class ItemDiscussion(models.Model):
    DISCUSSION_TYPES = [
        ('comment', 'Comentario'),
        ('question', 'Pregunta / Duda'),
    ]

    ITEM_TYPES = [
        ('anime', 'Anime'),
        ('manga', 'Manga'),
        ('lightnovel', 'Novela Ligera (MAL)'),
        ('original_novel', 'Novela Original'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    item_id = models.CharField(max_length=100, db_index=True)
    item_title = models.CharField(max_length=255, blank=True)
    discussion_type = models.CharField(max_length=20, choices=DISCUSSION_TYPES, default='comment')
    content = models.TextField(help_text="Contenido del comentario o pregunta")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Discusión / Comentario"
        verbose_name_plural = "Discusiones y Comentarios"
        ordering = ['created_at']

    def __str__(self):
        prefix = "Respuesta a" if self.parent else self.get_discussion_type_display()
        return f"{prefix} en {self.item_title or self.item_id} por {self.user.username}"


class Bookmark(models.Model):
    STATUS_CHOICES = [
        ('reading_watching', 'Leyendo / Viendo'),
        ('plan_to_read_watch', 'Por Leer / Ver'),
        ('completed', 'Completado'),
        ('favorite', 'Favorito'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    item_type = models.CharField(max_length=20)
    item_id = models.CharField(max_length=100, db_index=True)
    item_title = models.CharField(max_length=255)
    item_image = models.URLField(blank=True, max_length=500)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='favorite')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Marcador / Favorito"
        verbose_name_plural = "Marcadores y Favoritos"
        unique_together = ['user', 'item_type', 'item_id']

    def __str__(self):
        return f"{self.user.username} - {self.item_title} ({self.get_status_display()})"


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_review', 'En Revisión'),
        ('resolved', 'Resuelto'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_messages')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.subject}"


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.CharField(max_length=100, default='Comunidad')
    cover_image_url = models.URLField(blank=True, max_length=500)
    summary = models.TextField(help_text="Resumen breve para la tarjeta del blog")
    content = models.TextField(help_text="Contenido completo del artículo")
    views_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artículo de Blog"
        verbose_name_plural = "Artículos de Blog"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.title) or 'articulo'
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField(help_text="Comentario del usuario en el artículo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comentario de Blog"
        verbose_name_plural = "Comentarios de Blog"
        ordering = ['created_at']

    def __str__(self):
        return f"Comentario de @{self.user.username} en '{self.post.title}'"

