from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm

# Create your views here.
def index(request):
    return render(request, "index.html", { "user": request.user if request.user.is_authenticated else None })

def registerUser(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
    
    return render(request, "signup.html", { "form": form, "disabled_navbar_footer": True })

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
            

    return render(request, "signin.html", { "disabled_navbar_footer": True })

def logoutUser(request):
    logout(request)
    return redirect("index")