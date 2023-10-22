from django.urls import path
from django.contrib.auth import views as auth_view

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.registerUser, name="signup"),
    path("signin", views.loginUser, name="signin"),
    path("logout", views.logoutUser, name="logout"),
    path("movie/<int:movie_id>", views.movie, name="movie"),
    path("show/<int:show_id>", views.show, name="show"),
    path("book_show", views.bookShow, name="book_show"),
    path("bookings", views.bookings, name="bookings")
]