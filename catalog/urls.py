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

    # Tenrai API Gateway (Exposing 94 GET Endpoints)
    path('api/tenrai/random/<str:media_type>/', api_views.api_tenrai_random_view, name='api_tenrai_random'),
    path('api/tenrai/seasons/', api_views.api_tenrai_seasons_view, name='api_tenrai_seasons'),
    path('api/tenrai/schedules/', api_views.api_tenrai_schedules_view, name='api_tenrai_schedules'),
    path('api/tenrai/news/', api_views.api_tenrai_news_view, name='api_tenrai_news'),
    path('api/tenrai/articles/', api_views.api_tenrai_articles_view, name='api_tenrai_articles'),
    path('api/tenrai/stacks/', api_views.api_tenrai_stacks_view, name='api_tenrai_stacks'),
    path('api/tenrai/item/<str:media_type>/<str:item_id>/<str:extra>/', api_views.api_tenrai_item_extra_view, name='api_tenrai_item_extra'),
    path('api/tenrai/<path:path>', api_views.api_tenrai_proxy_view, name='api_tenrai_proxy'),

    # Sobre nosotros & Blog Oficial
    path('sobre-nosotros/quienes-somos/', pages_views.quienes_somos_view, name='quienes_somos'),
    path('sobre-nosotros/nuestra-historia/', pages_views.nuestra_historia_view, name='nuestra_historia'),
    path('sobre-nosotros/donde-estamos/', pages_views.donde_estamos_view, name='donde_estamos'),
    path('blog/', pages_views.blog_view, name='blog'),
    path('blog/crear/', pages_views.blog_create_view, name='blog_create'),
    path('blog/<slug:slug>/', pages_views.blog_detail_view, name='blog_detail'),
    path('blog/<slug:slug>/editar/', pages_views.blog_edit_view, name='blog_edit'),
    path('blog/<slug:slug>/eliminar/', pages_views.blog_delete_view, name='blog_delete'),

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
