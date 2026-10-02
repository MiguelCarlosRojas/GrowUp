from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from novels.models import Novel, Chapter, Category


class NovelsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(username='author1', password='password123')
        self.category = Category.objects.create(name='Isekai')

    def test_novel_and_chapter_creation_and_reading(self):
        self.client.login(username='author1', password='password123')
        # Create Novel
        response = self.client.post(reverse('novels:novel_create'), {
            'title': 'Crónicas del Hechicero Errante',
            'synopsis': 'Un joven despierta en un reino desconocido con habilidades mágicas arcanas.',
            'categories': [self.category.id],
            'status': 'ongoing',
            'demography': 'general',
            'language': 'Español',
        })
        self.assertEqual(response.status_code, 302)
        novel = Novel.objects.filter(title='Crónicas del Hechicero Errante').first()
        self.assertIsNotNone(novel)
        self.assertEqual(novel.author, self.author)

        # Add Chapter
        response = self.client.post(reverse('novels:chapter_create', kwargs={'novel_slug': novel.slug}), {
            'chapter_number': 1,
            'title': 'El Despertar',
            'content': 'Los rayos del sol se filtraban a través de las ramas del bosque encantado...',
            'author_notes': '¡Gracias por comenzar a leer mi novela!',
            'is_published': True,
        })
        self.assertEqual(response.status_code, 302)
        chapter = Chapter.objects.filter(novel=novel, chapter_number=1).first()
        self.assertIsNotNone(chapter)
        self.assertGreater(chapter.words_count, 0)

        # Read Chapter
        response = self.client.get(reverse('novels:chapter_read', kwargs={'novel_slug': novel.slug, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El Despertar")
        self.assertContains(response, "bosque encantado")

    def test_novel_detail_share_bar_and_list_view(self):
        novel = Novel.objects.create(
            author=self.author,
            title='Prueba de Novela con Compartir',
            slug='prueba-novela-compartir',
            synopsis='Sinopsis para probar botones de compartir en redes sociales.',
            status='ongoing',
            demography='general',
            language='Español'
        )
        response = self.client.get(reverse('novels:novel_detail', kwargs={'slug': novel.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compartir esta novela de la comunidad")
        self.assertContains(response, "WhatsApp")
        self.assertContains(response, "Facebook")
        self.assertContains(response, "Telegram")
        self.assertContains(response, "Copiar Enlace")

        # Test novel list view
        list_response = self.client.get(reverse('novels:novel_list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "Prueba de Novela con Compartir")
