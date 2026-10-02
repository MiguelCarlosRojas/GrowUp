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

    def test_user_login_with_email(self):
        User.objects.create_user(username='mixeduser', email='MyEmail@GrowUp.com', password='password123')
        # Login using email with mixed case
        response = self.client.post(reverse('accounts:login'), {
            'username': 'myemail@growup.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        # Login using username with mixed case
        response2 = self.client.post(reverse('accounts:login'), {
            'username': 'MixedUser',
            'password': 'password123'
        })
        self.assertEqual(response2.status_code, 302)

    def test_user_has_unique_uid(self):
        u1 = User.objects.create_user(username='user_uid_1', password='password123')
        u2 = User.objects.create_user(username='user_uid_2', password='password123')
        self.assertIsNotNone(u1.profile.uid)
        self.assertIsNotNone(u2.profile.uid)
        self.assertNotEqual(u1.profile.uid, u2.profile.uid)
        # Verify User.uid property
        self.assertEqual(u1.uid, str(u1.profile.uid))
        self.assertEqual(len(str(u1.profile.uid)), 36)

    def test_jwt_token_obtain_and_user_api(self):
        user = User.objects.create_user(username='jwt_user', password='password123', email='jwt@test.com')
        # Obtain tokens
        response = self.client.post(reverse('accounts:api_token_obtain'), {
            'username': 'jwt_user',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        tokens = data.get('tokens', {})
        self.assertIn('access_token', tokens)
        self.assertIn('refresh_token', tokens)
        self.assertEqual(tokens.get('user', {}).get('uid'), str(user.profile.uid))

        # Access protected endpoint with Bearer token
        access_token = tokens['access_token']
        auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        user_response = self.client.get(reverse('accounts:api_user_info'), **auth_headers)
        self.assertEqual(user_response.status_code, 200)
        user_data = user_response.json()
        self.assertEqual(user_data.get('user', {}).get('username'), 'jwt_user')
        self.assertEqual(user_data.get('user', {}).get('uid'), str(user.profile.uid))

    def test_jwt_token_refresh(self):
        User.objects.create_user(username='jwt_refresh_user', password='password123')
        obtain_resp = self.client.post(reverse('accounts:api_token_obtain'), {
            'username': 'jwt_refresh_user',
            'password': 'password123',
        })
        refresh_token = obtain_resp.json()['tokens']['refresh_token']

        refresh_resp = self.client.post(reverse('accounts:api_token_refresh'), {
            'refresh_token': refresh_token
        })
        self.assertEqual(refresh_resp.status_code, 200)
        self.assertIn('access_token', refresh_resp.json())

    def test_oauth_login_redirect(self):
        response = self.client.get(reverse('accounts:oauth_login', kwargs={'provider': 'google'}))
        # Redirects either to google OAuth URL or to login with warning if not configured
        self.assertIn(response.status_code, (302, 301))

    def test_profile_view_without_field_error(self):
        user = User.objects.create_user(username='reviewer_user', password='password123')
        from catalog.models import ItemReview
        ItemReview.objects.create(
            user=user,
            item_type='anime',
            item_id='52991',
            item_title='Frieren: Beyond Journey\'s End',
            rating=5,
            headline='Obra maestra absoluta',
            opinion='Una de las mejores historias de fantasía y reflexión.'
        )
        self.client.login(username='reviewer_user', password='password123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Frieren: Beyond Journey&#x27;s End')
        self.assertContains(response, 'Configuración de Perfil')

    def test_reader_dashboard_sidebar(self):
        user = User.objects.create_user(username='reader_user', password='password123')
        user.profile.role = 'reader'
        user.profile.save()
        self.client.login(username='reader_user', password='password123')

        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        # Should contain reader items
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'Opiniones y Calificación')
        self.assertContains(response, 'Preguntas, Respuestas y Debates')
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'Cerrar Sesión')
        # Should NOT contain author workshop
        self.assertNotContains(response, 'Mi Taller de Escritor')

    def test_author_dashboard_sidebar(self):
        user = User.objects.create_user(username='author_user', password='password123')
        user.profile.role = 'author'
        user.profile.save()
        self.client.login(username='author_user', password='password123')

        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        # Should contain author items including workshop
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'Opiniones y Calificación')
        self.assertContains(response, 'Preguntas, Respuestas y Debates')
        self.assertContains(response, 'Mi Taller de Escritor')
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'Cerrar Sesión')

    def test_dashboard_reviews_and_discussions_views(self):
        user = User.objects.create_user(username='community_user', password='password123')
        self.client.login(username='community_user', password='password123')

        # Test reviews page
        resp_reviews = self.client.get(reverse('accounts:dashboard_reviews'))
        self.assertEqual(resp_reviews.status_code, 200)
        self.assertContains(resp_reviews, 'Opiniones y Calificación')

        # Test discussions page
        resp_disc = self.client.get(reverse('accounts:dashboard_discussions'))
        self.assertEqual(resp_disc.status_code, 200)
        self.assertContains(resp_disc, 'Preguntas, Respuestas y Debates')


