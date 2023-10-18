from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signin(request):
    return render(request, 'signin.html', { "disabled_navbar_footer": True })

def signup(request):
    return render(request, 'signup.html', { "disabled_navbar_footer": True })