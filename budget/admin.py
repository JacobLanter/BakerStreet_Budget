from django.contrib import admin
from .models import Category

# this updates admin page to show the Category table in Django
admin.site.register(Category)
