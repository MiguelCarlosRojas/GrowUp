from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # OAuth 2.0 Endpoints
    path('oauth/<str:provider>/login/', views.oauth_login_view, name='oauth_login'),
    path('oauth/<str:provider>/callback/', views.oauth_callback_view, name='oauth_callback'),

    # JWT Authentication Endpoints
    path('api/token/', views.api_token_obtain_view, name='api_token_obtain'),
    path('api/token/refresh/', views.api_token_refresh_view, name='api_token_refresh'),
    path('api/user/', views.api_user_info_view, name='api_user_info'),
]

