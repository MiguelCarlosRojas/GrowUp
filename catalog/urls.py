from django.urls import path
from . import views
from . import pages_views
from . import api_views

app_name = 'catalog'

urlpatterns = [
    # Catalog Core
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('detail/<str:item_type>/<str:item_id>/', views.item_detail_view, name='item_detail'),
    path('review/<str:item_type>/<str:item_id>/', views.add_review_view, name='add_review'),
    path('discussion/<str:item_type>/<str:item_id>/', views.add_discussion_view, name='add_discussion'),
    path('bookmark/<str:item_type>/<str:item_id>/', views.toggle_bookmark_view, name='toggle_bookmark'),

    # Optimized Single-Query REST Endpoints
    path('api/novels/', api_views.api_novels_optimized_view, name='api_novels'),
    path('api/live/metrics/', api_views.api_live_metrics_view, name='api_live_metrics'),
    path('api/live/notifications/', api_views.api_live_notifications_view, name='api_live_notifications'),
    path('ws/live/', api_views.ws_live_http_fallback_view, name='ws_live_fallback'),

    # Sobre nosotros
    path('sobre-nosotros/quienes-somos/', pages_views.quienes_somos_view, name='quienes_somos'),
    path('sobre-nosotros/nuestra-historia/', pages_views.nuestra_historia_view, name='nuestra_historia'),
    path('sobre-nosotros/donde-estamos/', pages_views.donde_estamos_view, name='donde_estamos'),
    path('blog/', pages_views.blog_view, name='blog'),

    # Ayuda & Contacto
    path('ayuda/', pages_views.ayuda_view, name='ayuda'),
    path('ayuda/preguntas-frecuentes/', pages_views.preguntas_frecuentes_view, name='preguntas_frecuentes'),
    path('contacto/', pages_views.contacto_view, name='contacto'),

    # Legal & Privacidad
    path('legal/aviso-legal/', pages_views.aviso_legal_view, name='aviso_legal'),
    path('legal/politica-cookies/', pages_views.politica_cookies_view, name='politica_cookies'),
    path('legal/condiciones-uso/', pages_views.condiciones_uso_view, name='condiciones_uso'),
    path('legal/politica-privacidad/', pages_views.politica_privacidad_view, name='politica_privacidad'),
    path('legal/declaracion-accesibilidad/', pages_views.declaracion_accesibilidad_view, name='declaracion_accesibilidad'),
]
