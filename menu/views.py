from django.http import HttpRequest
from django.shortcuts import render
from .models import MenuItem, Menu
# Create your views here.


def get_menu(request: HttpRequest, menu_pk):
    menu_item_pk = request.GET.get("menu_item_pk")
    return render(request, "menu/index.html", {"menu_pk": menu_pk, "menu_item_pk": menu_item_pk})

def menu_list(request: HttpRequest):
    menus = Menu.objects.all()
    return render(request, "menu/menus.html", {"menu_list": menus})