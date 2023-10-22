from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Movie, MoviesGenresLink, Show
import datetime


# Create your views here.
def index(request):
    movies = Movie.objects.all()

    return render(
        request,
        "index.html",
        {
            "user": request.user if request.user.is_authenticated else None,
            "navbar_fixed_top": "fixed-top",
            "movies": movies,
        },
    )


def registerUser(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")

    return render(
        request, "signup.html", {"form": form, "disabled_navbar_footer": True}
    )


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Username or password is incorrect.")

        else:
            messages.error(request, "Fill out all the fields.")

    return render(request, "signin.html", {"disabled_navbar_footer": True})


def logoutUser(request):
    logout(request)
    return redirect("index")


def movie(request, movie_id):

    selected_date = request.GET.get('selected_date', None)

    current_date = datetime.datetime.now()

    if selected_date:
        current_year = datetime.datetime.now().year
        current_date = datetime.datetime.strptime(f"{selected_date} {current_year}", '%d %b %Y')

        serialized_shows = [
            {
                "pk": show.pk,
                "hour": show.timing.hour,
                "minute": show.timing.minute
            }
            for show in Show.objects.filter(movie_id=movie_id, timing__date=current_date.date()).order_by("timing")
        ]

        return JsonResponse({
            "count": len(serialized_shows),
            "shows": serialized_shows
        })

    movie = Movie.objects.get(pk=movie_id)
    genres = MoviesGenresLink.objects.filter(movie__lte=movie_id)
    shows = Show.objects.filter(movie_id=movie_id, timing__date=current_date.date()).order_by("timing")

    date_array = [
        (current_date + datetime.timedelta(days=i)).strftime("%d %b")
        for i in range(5)
    ]

    return render(
        request,
        "movie.html",
        {
            "movie": movie,
            "genres": genres,
            "show_dates": date_array,
            "current_date": current_date.strftime("%d %b"),
            "shows": shows
        },
    )
