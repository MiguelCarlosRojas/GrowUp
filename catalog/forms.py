from django import forms
from .models import ItemReview, ItemDiscussion

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
