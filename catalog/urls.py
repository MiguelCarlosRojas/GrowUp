from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('detail/<str:item_type>/<str:item_id>/', views.item_detail_view, name='item_detail'),
    path('review/<str:item_type>/<str:item_id>/', views.add_review_view, name='add_review'),
    path('discussion/<str:item_type>/<str:item_id>/', views.add_discussion_view, name='add_discussion'),
    path('bookmark/<str:item_type>/<str:item_id>/', views.toggle_bookmark_view, name='toggle_bookmark'),
]
