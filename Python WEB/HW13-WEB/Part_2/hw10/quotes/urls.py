from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('tag/<str:tag_name>/', views.tag_page, name='tag_page'),
    path('author/<str:fullname>/', views.author_page, name='author_page'),
    path('top_tags', views.top_tags, name='top_tags')
]