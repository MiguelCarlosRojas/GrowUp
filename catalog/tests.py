from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
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
