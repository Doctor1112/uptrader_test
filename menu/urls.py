from django.contrib import admin
from django.urls import path
from .views import get_menu, menu_list

urlpatterns = [
    path('<str:menu_pk>/', get_menu, name="menu"),
    path("", menu_list, name="menu_list")
]