from django.contrib import admin
from .models import *

# List of models to register
models_to_register = [Movie, Genre, MoviesGenresLink, Show, Booking]

# Register all models
for model in models_to_register:
    admin.site.register(model)
