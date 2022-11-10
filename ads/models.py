from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


class Ads(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    author = models.CharField(max_length=50, verbose_name='Автор')
    price = models.IntegerField(verbose_name='Стоимость')
    description = models.CharField(max_length=1000, verbose_name='Описание')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    is_published = models.BooleanField(verbose_name='Опубликовано')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class AdsEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Ads):
            return {'id': o.id,
                    'name': o.name,
                    'author': o.author,
                    'price': o.price,
                    'description': o.description,
                    'address': o.address,
                    'is_published': o.is_published}
        return super().default(o)


class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class CatEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Categories):
            return {'id': o.id,
                    'name': o.name}
        return super().default(o)
