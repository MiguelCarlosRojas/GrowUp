from django import forms
from .models import ItemReview, ItemDiscussion, ContactMessage, BlogPost, BlogComment

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (5, '5 de 5 - Obra Maestra'),
        (4, '4 de 5 - Muy Bueno'),
        (3, '3 de 5 - Bueno'),
        (2, '2 de 5 - Regular'),
        (1, '1 de 5 - Malo')
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Tu Clasificación"
    )

    class Meta:
        model = ItemReview
        fields = ['rating', 'headline', 'opinion']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Una trama fascinante e inolvidable'}),
            'opinion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu opinión sincera sobre los personajes, desarrollo, animación o narrativa...'}),
        }


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = ItemDiscussion
        fields = ['discussion_type', 'content']
        widgets = {
            'discussion_type': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Haz una pregunta sobre la historia o deja un comentario respetuoso...'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-pro',
                'placeholder': 'Tu nombre o seudónimo',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-pro',
                'placeholder': 'correo@ejemplo.com',
                'required': True,
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control form-control-pro',
                'placeholder': 'Motivo de tu consulta o sugerencia',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control form-control-pro',
                'rows': 5,
                'placeholder': 'Detalla tu duda, reporte o propuesta para el equipo de GrowUp...',
                'required': True,
            }),
        }


class BlogPostForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('Novedades', 'Novedades de la Plataforma'),
        ('Comunidad', 'Comunidad y Eventos'),
        ('Recomendaciones', 'Recomendaciones Anime & Manga'),
        ('Autores', 'Consejos para Autores y Escritores'),
        ('Tecnología', 'Arquitectura y Tecnología'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-control-pro'}),
        label="Categoría"
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'cover_image_url', 'summary', 'content', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-pro',
                'placeholder': 'Título atractivo del artículo',
                'required': True,
            }),
            'cover_image_url': forms.URLInput(attrs={
                'class': 'form-control form-control-pro',
                'placeholder': 'https://ejemplo.com/portada.jpg (Opcional)',
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control form-control-pro',
                'rows': 3,
                'placeholder': 'Breve sinopsis o introducción que aparecerá en la tarjeta del listado...',
                'required': True,
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control form-control-pro font-monospace',
                'rows': 12,
                'placeholder': 'Escribe el contenido completo del artículo (soporta párrafos, listas y texto estructurado)...',
                'required': True,
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control form-control-pro',
                'rows': 3,
                'placeholder': 'Escribe tu comentario u opinión sobre este artículo...',
                'required': True,
            }),
        }

