from django.urls import path
from . import views

app_name = 'novels'

urlpatterns = [
    path('', views.novel_list, name='novel_list'),
    path('dashboard/', views.author_dashboard, name='author_dashboard'),
    path('create/', views.novel_create, name='novel_create'),
    path('<slug:slug>/', views.novel_detail, name='novel_detail'),
    path('<slug:slug>/edit/', views.novel_edit, name='novel_edit'),
    path('<slug:novel_slug>/chapter/add/', views.chapter_create, name='chapter_create'),
    path('<slug:novel_slug>/chapter/<str:chapter_number>/', views.chapter_read, name='chapter_read'),
    path('<slug:novel_slug>/chapter/<str:chapter_number>/edit/', views.chapter_edit, name='chapter_edit'),
]
