from django.db import models
from django.urls import reverse,NoReverseMatch

#todo нельзя выбрать родителем себя, и нельзя зациклить (в родителях у обих выбрать обоих)

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='child')
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=200, blank=True)

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'

    def __str__(self):
        return self.title