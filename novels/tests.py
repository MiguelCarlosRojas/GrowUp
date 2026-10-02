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
        # Verifies sequential redirection from novel creation directly to chapter creation
        self.assertRedirects(response, reverse('novels:chapter_create', kwargs={'novel_slug': novel.slug}))

        # Add Chapter
        response = self.client.post(reverse('novels:chapter_create', kwargs={'novel_slug': novel.slug}), {
            'chapter_number': 1,
            'title': 'El Despertar',
            'content': 'Los rayos del sol se filtraban a través de las ramas del bosque encantado...',
            'author_notes': 'Gracias por comenzar a leer mi novela',
            'is_published': True,
        })
        self.assertEqual(response.status_code, 302)
        chapter = Chapter.objects.filter(novel=novel, chapter_number=1).first()
        self.assertIsNotNone(chapter)
        self.assertGreater(chapter.words_count, 0)
        self.assertIsNotNone(chapter.created_at)

        # Read Chapter as author (should see Creado el)
        response = self.client.get(reverse('novels:chapter_read', kwargs={'novel_slug': novel.slug, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El Despertar")
        self.assertContains(response, "bosque encantado")
        self.assertContains(response, "Creado:")

        # Read Chapter as anonymous public reader (should NOT see Creado)
        self.client.logout()
        pub_response = self.client.get(reverse('novels:chapter_read', kwargs={'novel_slug': novel.slug, 'chapter_number': 1}))
        self.assertEqual(pub_response.status_code, 200)
        self.assertContains(pub_response, "Publicado:")
        self.assertNotContains(pub_response, "Creado:")

    def test_workspace_isolation_in_novel_and_chapter_forms(self):
        self.client.login(username='author1', password='password123')
        # Novel form should render inside user workspace shell
        resp_novel = self.client.get(reverse('novels:novel_create'))
        self.assertEqual(resp_novel.status_code, 200)
        self.assertContains(resp_novel, 'Workspace de Usuario')
        self.assertContains(resp_novel, 'app-sidebar-v2')

        novel = Novel.objects.create(
            author=self.author,
            title='Obra en Workspace',
            slug='obra-en-workspace',
            synopsis='Sinopsis de prueba',
            status='draft'
        )
        # Chapter form should also render inside workspace shell
        resp_chapter = self.client.get(reverse('novels:chapter_create', kwargs={'novel_slug': novel.slug}))
        self.assertEqual(resp_chapter.status_code, 200)
        self.assertContains(resp_chapter, 'Workspace de Usuario')
        self.assertContains(resp_chapter, 'Guardar y Finalizar')

    def test_novel_visibility_toggle(self):
        self.client.login(username='author1', password='password123')
        novel = Novel.objects.create(
            author=self.author,
            title='Novela Secreta',
            slug='novela-secreta',
            synopsis='Sinopsis privada',
            status='draft'
        )
        # Should be excluded from public catalogue when draft
        list_resp = self.client.get(reverse('novels:novel_list'))
        self.assertNotContains(list_resp, 'Novela Secreta')

        # Toggle to public
        toggle_resp = self.client.post(reverse('novels:toggle_novel_visibility', kwargs={'slug': novel.slug}))
        self.assertRedirects(toggle_resp, reverse('novels:author_dashboard'))
        novel.refresh_from_db()
        self.assertEqual(novel.status, 'ongoing')

        # Now appears in public catalogue
        list_resp2 = self.client.get(reverse('novels:novel_list'))
        self.assertContains(list_resp2, 'Novela Secreta')

        # Toggle back to private (draft)
        self.client.post(reverse('novels:toggle_novel_visibility', kwargs={'slug': novel.slug}))
        novel.refresh_from_db()
        self.assertEqual(novel.status, 'draft')

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
