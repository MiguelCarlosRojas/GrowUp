from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testwriter',
            'email': 'writer@growup.com',
            'first_name': 'Carlos',
            'last_name': 'Rojas',
            'role': 'author',
            'password': 'StrongPassword123!',
            'password_confirm': 'StrongPassword123!',
            'bio': 'Escritor de novelas ligeras de fantasía.',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.filter(username='testwriter').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.profile.role, 'author')
        self.assertTrue(user.profile.is_author)

    def test_user_login_and_logout(self):
        user = User.objects.create_user(username='testreader', password='password123')
        # Login
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testreader',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        # Logout
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
