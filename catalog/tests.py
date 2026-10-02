from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from catalog.models import ItemReview, ItemDiscussion


class CatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='otaku_master', password='password123')

    def test_home_page_status(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GrowUp")
        self.assertContains(response, "Animes en Tendencia & Aclamados")

    def test_explore_page_status_and_filters(self):
        response = self.client.get(reverse('catalog:explore') + '?type=manga&q=Berserk')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Berserk")

    def test_item_detail_and_review_creation(self):
        self.client.login(username='otaku_master', password='password123')
        # Post review
        response = self.client.post(
            reverse('catalog:add_review', kwargs={'item_type': 'anime', 'item_id': '5114'}),
            {
                'item_title': 'Fullmetal Alchemist: Brotherhood',
                'item_image': 'https://cdn.myanimelist.net/images/anime/1208/94745l.jpg',
                'rating': 5,
                'headline': 'Una obra de arte absoluta',
                'opinion': 'El mejor shonen de todos los tiempos, historia cerrada sin relleno.',
            }
        )
        self.assertEqual(response.status_code, 302)
        review = ItemReview.objects.filter(item_id='5114', user=self.user).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 5)

    def test_item_discussion_and_reply(self):
        self.client.login(username='otaku_master', password='password123')
        response = self.client.post(
            reverse('catalog:add_discussion', kwargs={'item_type': 'anime', 'item_id': '5114'}),
            {
                'item_title': 'Fullmetal Alchemist: Brotherhood',
                'discussion_type': 'question',
                'content': '¿En qué orden recomiendan ver la versión de 2003 vs Brotherhood?',
            }
        )
        self.assertEqual(response.status_code, 302)
        disc = ItemDiscussion.objects.filter(item_id='5114', user=self.user).first()
        self.assertIsNotNone(disc)
        self.assertEqual(disc.discussion_type, 'question')

    def test_corporate_and_legal_pages(self):
        page_names = [
            'catalog:quienes_somos',
            'catalog:nuestra_historia',
            'catalog:donde_estamos',
            'catalog:blog',
            'catalog:ayuda',
            'catalog:preguntas_frecuentes',
            'catalog:contacto',
            'catalog:aviso_legal',
            'catalog:politica_cookies',
            'catalog:condiciones_uso',
            'catalog:politica_privacidad',
            'catalog:declaracion_accesibilidad',
            'accounts:login',
            'accounts:register',
        ]
        for name in page_names:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, f"Page {name} returned status {response.status_code}")

    @patch('catalog.services.jikan_service.get_item_detail')
    def test_platforms_and_social_sharing_in_item_detail(self, mock_get_item):
        mock_get_item.return_value = {
            'mal_id': 52991,
            'title': "Sousou no Frieren",
            'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/anime/1015/138062l.jpg'}},
            'synopsis': "Durante su viaje de una década para derrotar al Rey Demonio...",
            'score': 9.3,
            'type': 'TV',
            'status': 'Finalizado',
            'genres': [{'name': 'Aventura'}, {'name': 'Fantasía'}],
        }
        response = self.client.get(reverse('catalog:item_detail', kwargs={'item_type': 'anime', 'item_id': '52991'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compartir esta obra")
        self.assertContains(response, "WhatsApp")
        self.assertContains(response, "Facebook")
        self.assertContains(response, "Telegram")
        self.assertContains(response, "Copiar Enlace")
        self.assertContains(response, "Plataformas Oficiales")
        self.assertContains(response, "Plataformas Comunitarias")

    def test_explore_pagination_structure(self):
        response = self.client.get(reverse('catalog:explore') + '?type=anime&page=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pagination', response.context)
        self.assertEqual(response.context['pagination']['per_page'], 24)
        self.assertContains(response, "Resultados")

    def test_api_novels_optimized_single_query(self):
        response = self.client.get(reverse('catalog:api_novels'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('items', data)

    def test_api_live_metrics(self):
        response = self.client.get(reverse('catalog:api_live_metrics'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('metrics', data)
        self.assertIn('total_novels', data['metrics'])
        self.assertIn('total_views', data['metrics'])

    def test_toast_notification_container_present(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'toastNotificationContainer')
        self.assertContains(response, 'toast-popup-container')


