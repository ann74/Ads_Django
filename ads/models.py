from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError

from authentication.models import User


def not_published(value):
    if value is True:
        raise ValidationError('is_published не может быть True')


class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.CharField(max_length=10, null=True, unique=True, validators=[MinLengthValidator(5)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ads(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тема', validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    price = models.IntegerField(verbose_name='Стоимость', validators=[MinValueValidator(0)])
    description = models.CharField(max_length=1000, default='', null=True, verbose_name='Описание')
    is_published = models.BooleanField(verbose_name='Опубликовано', validators=[not_published])
    image = models.ImageField(upload_to='images/', null=True, verbose_name='Изображение')
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-price']


class AdsSelection(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    items = models.ManyToManyField(Ads, verbose_name='Объявление')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'


class CatEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Categories):
            return {'id': o.id,
                    'name': o.name,
                    'slug': o.slug}
        return super().default(o)
