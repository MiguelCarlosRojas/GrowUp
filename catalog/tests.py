from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch

from catalog.models import ItemReview, ItemDiscussion
from catalog.services import jikan_service


class CatalogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='otaku_master', password='password123')

    @patch('catalog.views.jikan_service.get_common_genres', return_value=[])
    @patch('catalog.views.jikan_service.get_top_lightnovels', return_value=[])
    @patch('catalog.views.jikan_service.get_top_manga', return_value=[])
    @patch('catalog.views.jikan_service.get_top_anime', return_value=[])
    def test_home_page_status(self, *_):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GrowUp")
        self.assertContains(response, "Animes en Tendencia & Aclamados")

    @patch('catalog.views.jikan_service.get_common_genres', return_value=[])
    @patch('catalog.views.jikan_service.search_items')
    def test_explore_page_status_and_filters(self, mock_search_items, *_):
        mock_search_items.return_value = {
            'items': [
                {
                    'mal_id': 2,
                    'title': 'Berserk',
                    'images': {'jpg': {'large_image_url': 'https://cdn.myanimelist.net/images/manga/1/157897l.jpg'}},
                    'type': 'Manga',
                    'status': 'Publishing',
                }
            ],
            'pagination': {},
        }
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

    @patch('catalog.services.jikan_service._safe_request', return_value=None)
    def test_jikan_service_strict_without_api_data(self, _):
        self.assertEqual(jikan_service.get_top_anime(), [])
        self.assertEqual(jikan_service.get_top_manga(), [])
        self.assertEqual(jikan_service.get_top_lightnovels(), [])
        self.assertEqual(jikan_service.search_items(category='anime', query='Berserk')['items'], [])
        self.assertEqual(jikan_service.get_common_genres(), [])
        self.assertIsNone(jikan_service.get_item_detail('anime', 1))
