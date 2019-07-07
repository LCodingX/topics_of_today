from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="infos-home"),
    path('Fields/', views.fields, name="infos-fields"),
    path('Field/<int:pk>/', views.field, name="infos-field"),
    path('Topics/', views.topics, name="infos-topics"),
    path('Trending/', views.trending, name="infos-trending"),
    path('upload/postimg/<int:pk>/', views.uploadpostimg, name="upload-postimg"),
    path('Post/<int:pk>/', views.post.as_view(), name="infos-post"),
    path("Post/<int:pk>/update/", views.UpdatePostView.as_view(), name="update-post"),
    path('Topic/<int:pk>/', views.topic.as_view(), name="infos-topic"),
    path('Topics/create/', views.create_topic, name="infos-create-topic"),
    path('Posts/create/', views.create_post.as_view(), name="infos-create-post"),
    path("search/all/", views.searchall, name="search-all"),
    path("search/topics/", views.searchtopics, name="search-all"),
    path("search/posts/", views.searchposts, name="search-all"),
    path("search/in/<int:pk>/", views.searchin, name="search-all"),
    path('search/users/<int:pk>/', views.searchuser, name="search-user"),
    path("Comment/<int:pk>/", views.comment, name="infos-comment"),
    path("delete/post/<int:pk>/", views.deletepost, name="delete-post"),
    path("like/post/<int:pk>/", views.like, name="like-post"),
    path("unlike/post/<int:pk>/", views.unlike, name="unlike-post"),

]