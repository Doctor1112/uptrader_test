from django.db import models
from django.urls import reverse


class Menu(models.Model):

    title = models.CharField(primary_key=True, max_length=150)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("menu", args=[self.pk])

class MenuItem(models.Model):

    content = models.TextField()
    parent = models.ForeignKey("MenuItem", on_delete=models.CASCADE, blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'{reverse("menu", args=[self.menu.pk])}?menu_item_pk={self.pk}'
    
    def __str__(self) -> str:
        return self.content
    

