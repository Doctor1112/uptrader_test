from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse, reverse_lazy
from .models import MenuItem, Menu
from django.utils.html import format_html
# Register your models here.


class BaseMenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    def admin_link(self, instance):
        url = f'/admin/menu/menuitem/{instance.id}/change/'
        return format_html(u'<a href="{}">Edit</a>', url)
    
    readonly_fields = ('admin_link',)

class MenuItemInline(BaseMenuItemInline):
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['menu'].initial = obj.menu

        return formset


class MenuItemInMenuInline(BaseMenuItemInline):

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['menu'].initial = obj

        return formset
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(parent=None)

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('content', 'parent')
    list_filter = ('parent',)
    inlines = [MenuItemInline]

class MenuAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [MenuItemInMenuInline]

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu, MenuAdmin)
