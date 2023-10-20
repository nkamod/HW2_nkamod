from django.urls import path
from django.contrib.auth import views as auth_view

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.registerUser, name="signup"),
    path("signin", views.loginUser, name="signin"),
    path("logout", views.logoutUser, name="logout")
]