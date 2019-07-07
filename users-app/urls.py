from django.urls import path
from . import views as userviews
from django.contrib.auth import views as authviews
urlpatterns = [
    path('register/', userviews.register, name="users-register"),
    path('login/', authviews.LoginView.as_view(template_name="users/login.html"), name="users-login"),
    path('logout/', authviews.LogoutView.as_view(template_name="users/logout.html"), name="users-logout"),
    path("profile/", userviews.profile, name="users-profile"),
    path('profile/inbox/', userviews.inbox, name="users-inbox")
]