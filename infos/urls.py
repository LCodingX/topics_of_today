from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="infos-home"),
    path('Topics/', views.topics, name="infos-topics"),
    path('Trending/', views.trending, name="infos-trending"),
    path('Post/<int:pk>/', views.post.as_view(), name="infos-post")
]