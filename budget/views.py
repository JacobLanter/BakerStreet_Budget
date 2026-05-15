from django.shortcuts import render
from .models import Category

def category_list(request):
    categories = Category.objects.all()

    return render(request, "budget/category_list.html", {"categories" : categories},)
