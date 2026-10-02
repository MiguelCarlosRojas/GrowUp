from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría / Género"
        verbose_name_plural = "Categorías / Géneros"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Novel(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'En Emisión'),
        ('completed', 'Finalizada'),
        ('hiatus', 'En Pausa'),
        ('draft', 'Borrador'),
    ]

    DEMOGRAPHY_CHOICES = [
        ('shonen', 'Shonen'),
        ('seinen', 'Seinen'),
        ('shoujo', 'Shoujo'),
        ('josei', 'Josei'),
        ('general', 'General'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='novels')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    synopsis = models.TextField(help_text="Sinopsis y descripción de la novela ligera")
    cover_image = models.ImageField(upload_to='novels/covers/', blank=True, null=True)
    cover_url = models.URLField(
        blank=True,
        default="https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500",
        help_text="URL externa de la portada si no sube archivo"
    )
    categories = models.ManyToManyField(Category, related_name='novels', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    demography = models.CharField(max_length=20, choices=DEMOGRAPHY_CHOICES, default='general')
    language = models.CharField(max_length=30, default='Español')
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Novela Ligera"
        verbose_name_plural = "Novelas Ligeras"
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "novela"
            slug = base_slug
            count = 1
            while Novel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def final_cover(self):
        if self.cover_image:
            return self.cover_image.url
        return self.cover_url or "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500"

    def published_chapters(self):
        return self.chapters.filter(is_published=True).order_by('chapter_number')

    def get_absolute_url(self):
        return reverse('novels:novel_detail', kwargs={'slug': self.slug})


class Chapter(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='chapters')
    chapter_number = models.FloatField(help_text="Ej: 1, 2, 2.5")
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Texto completo del capítulo")
    author_notes = models.TextField(blank=True, help_text="Notas o comentarios del autor")
    is_published = models.BooleanField(default=True)
    words_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Capítulo"
        verbose_name_plural = "Capítulos"
        ordering = ['chapter_number']
        unique_together = ['novel', 'chapter_number']

    def save(self, *args, **kwargs):
        if self.content:
            self.words_count = len(self.content.split())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.novel.title} - Cap {self.chapter_number}: {self.title}"

    def get_next_chapter(self):
        return self.novel.chapters.filter(
            is_published=True,
            chapter_number__gt=self.chapter_number
        ).order_by('chapter_number').first()

    def get_previous_chapter(self):
        return self.novel.chapters.filter(
            is_published=True,
            chapter_number__lt=self.chapter_number
        ).order_by('-chapter_number').first()
