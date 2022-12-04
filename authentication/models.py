from django.contrib.auth.models import AbstractUser
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name='Адрес')
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, verbose_name='Широта')
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True, verbose_name='Долгота')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class User(AbstractUser):
    ROLE = [
        ('member', 'Участник'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    ]

    role = models.CharField(max_length=20, choices=ROLE, default='member', verbose_name='Роль')
    age = models.IntegerField(null=True, verbose_name='Возраст')
    locations = models.ManyToManyField(Location, verbose_name='Адрес')
    birthday = models.DateField(null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
