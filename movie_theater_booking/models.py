from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=300)
    poster = models.CharField(max_length=500)
    trailer = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    rating = models.FloatField()
    cast = models.CharField(max_length=100) # Json string
    runtime = models.IntegerField() # In minutes
    release_year = models.IntegerField(default=None)

class Genre(models.Model):
    title = models.CharField(max_length=100)

class MoviesGenresLink(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
class Show(models.Model):
    timing = models.DateTimeField()
    price = models.FloatField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Booking(models.Model):
    date = models.DateTimeField()
    seat_no = models.CharField(max_length=5)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)