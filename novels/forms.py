from django import forms
from .models import Novel, Chapter, Category


class NovelForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Categorías / Géneros"
    )

    class Meta:
        model = Novel
        fields = ['title', 'synopsis', 'cover_image', 'cover_url', 'categories', 'status', 'demography', 'language']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: El Despertar del Héroe Supremo'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe el argumento y trama principal de tu novela ligera...'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com/portada.jpg (Opcional)'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'demography': forms.Select(attrs={'class': 'form-select'}),
            'language': forms.TextInput(attrs={'class': 'form-control', 'value': 'Español'}),
        }


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_number', 'title', 'content', 'author_notes', 'is_published']
        widgets = {
            'chapter_number': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '1'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Prólogo: Una segunda oportunidad'}),
            'content': forms.Textarea(attrs={'class': 'form-control font-monospace', 'rows': 16, 'placeholder': 'Escribe o pega aquí el contenido completo del capítulo...'}),
            'author_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas para los lectores (agradecimientos, anuncios, etc.)'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
