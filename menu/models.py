from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse,NoReverseMatch


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

    def clean(self):
        if self.parent == self:
            raise ValidationError('Нельзя выбрать родителем самого себя')

        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError('Нельзя создавать цикл')
            parent = parent.parent

        if not self.url and not self.named_url:
            raise ValidationError('Одно из полей URL, либо named URL должно быть заполнено')

        if self.named_url:
            try:
                reverse(self.named_url)
            except NoReverseMatch:
                raise ValidationError(f'Указанный named URL "{self.named_url}" не существует')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)