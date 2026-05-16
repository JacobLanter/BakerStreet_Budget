from django.urls import path
from . import views

urlpatterns = [
    path('category_list/', views.category_list, name="category_list"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path("sync-ynab/", views.sync_ynab_now, name="sync_ynab_now"),
]
