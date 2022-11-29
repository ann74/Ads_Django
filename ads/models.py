from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

from authentication.models import User


class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ads(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тема')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    price = models.IntegerField(verbose_name='Стоимость')
    description = models.CharField(max_length=1000, default='', null=True, verbose_name='Описание')
    is_published = models.BooleanField(verbose_name='Опубликовано')
    image = models.ImageField(upload_to='images/', null=True, verbose_name='Изображение')
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-price']


class CatEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Categories):
            return {'id': o.id,
                    'name': o.name}
        return super().default(o)
