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
        self.assertContains(response, 'Mi Perfil')
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
        self.assertContains(response, 'Mi Perfil')
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

    def test_author_reviews_and_discussions_segregated_sessions(self):
        from catalog.models import ItemReview, ItemDiscussion
        from novels.models import Novel

        author = User.objects.create_user(username='author_creator', password='password123')
        author.profile.role = 'author'
        author.profile.save()

        reader = User.objects.create_user(username='reader_fan', password='password123')
        reader.profile.role = 'reader'
        reader.profile.save()

        novel = Novel.objects.create(
            author=author,
            title='La Leyenda del Nigromante',
            slug='leyenda-nigromante',
            synopsis='Sinopsis épica',
            status='ongoing'
        )

        # Reader leaves review on author's novel
        ItemReview.objects.create(
            user=reader,
            item_type='original_novel',
            item_id=novel.slug,
            item_title=novel.title,
            rating=5,
            headline='Excelente inicio',
            opinion='Me encanto la construccion de mundo y el protagonista.'
        )

        # Author leaves review on an external anime
        ItemReview.objects.create(
            user=author,
            item_type='anime',
            item_id='1',
            item_title='Cowboy Bebop',
            rating=4,
            headline='Clasico indispensable',
            opinion='Una joya de la animacion de los 90s.'
        )

        # Reader leaves question on author's novel
        ItemDiscussion.objects.create(
            user=reader,
            item_type='original_novel',
            item_id=novel.slug,
            item_title=novel.title,
            discussion_type='question',
            content='¿Con que frecuencia se publicaran los siguientes capitulos?'
        )

        # Login as author
        self.client.login(username='author_creator', password='password123')

        # Reviews view for author
        resp_rev = self.client.get(reverse('accounts:dashboard_reviews'))
        self.assertEqual(resp_rev.status_code, 200)
        self.assertContains(resp_rev, 'Panel de Escritor')
        self.assertContains(resp_rev, 'Reseñas Recibidas en mis Novelas')
        self.assertContains(resp_rev, 'Mis Opiniones a otras Obras')
        self.assertContains(resp_rev, 'Excelente inicio')
        self.assertContains(resp_rev, 'Cowboy Bebop')

        # Discussions view for author
        resp_disc = self.client.get(reverse('accounts:dashboard_discussions'))
        self.assertEqual(resp_disc.status_code, 200)
        self.assertContains(resp_disc, 'Panel de Escritor')
        self.assertContains(resp_disc, 'Preguntas y Debates de Lectores en mis Obras')
        self.assertContains(resp_disc, '¿Con que frecuencia se publicaran los siguientes capitulos?')

    def test_reader_reviews_and_discussions_breakdown(self):
        from catalog.models import ItemReview, ItemDiscussion

        reader = User.objects.create_user(username='reader_critic', password='password123')
        reader.profile.role = 'reader'
        reader.profile.save()

        ItemReview.objects.create(
            user=reader,
            item_type='manga',
            item_id='100',
            item_title='Berserk',
            rating=5,
            headline='Obra cumbre',
            opinion='Inigualable en arte y trama.'
        )

        q = ItemDiscussion.objects.create(
            user=reader,
            item_type='anime',
            item_id='200',
            item_title='Steins;Gate',
            discussion_type='question',
            content='¿En que orden cronologico se deben ver los episodios especiales?'
        )

        self.client.login(username='reader_critic', password='password123')

        resp_rev = self.client.get(reverse('accounts:dashboard_reviews'))
        self.assertEqual(resp_rev.status_code, 200)
        self.assertContains(resp_rev, 'Perfil Lector')
        self.assertContains(resp_rev, '5 Estrellas')
        self.assertContains(resp_rev, 'Berserk')

        resp_disc = self.client.get(reverse('accounts:dashboard_discussions'))
        self.assertEqual(resp_disc.status_code, 200)
        self.assertContains(resp_disc, 'Perfil Lector')
        self.assertContains(resp_disc, 'Mis Preguntas Formuladas')
        self.assertContains(resp_disc, 'En Animes')
        self.assertContains(resp_disc, 'Steins;Gate')

    def test_user_navbar_dropdown_simplified(self):
        user = User.objects.create_user(username='nav_tester', password='password123')
        self.client.login(username='nav_tester', password='password123')
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi Perfil')
        self.assertContains(response, 'Cerrar Sesión')
        self.assertContains(response, 'user-nav-pill-btn')
        # Navbar dropdown should NOT contain the old extra links
        self.assertNotContains(response, 'Mi Dashboard')

    def test_uid_hidden_from_profile_and_dashboard(self):
        user = User.objects.create_user(username='uid_tester', password='password123')
        self.client.login(username='uid_tester', password='password123')
        
        # In profile view, visible UID text should NOT be present
        resp_prof = self.client.get(reverse('accounts:profile'))
        self.assertEqual(resp_prof.status_code, 200)
        self.assertNotContains(resp_prof, f"UID: {user.profile.uid}")
        
        # In dashboard view, visible UID text should NOT be present
        resp_dash = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(resp_dash.status_code, 200)
        self.assertNotContains(resp_dash, f"UID: {user.profile.uid}")



