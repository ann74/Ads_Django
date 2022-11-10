from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name='Адрес')
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, verbose_name='Широта')
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True, verbose_name='Долгота')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Users(models.Model):
    ROLE = [
        ('member', 'Участник'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    ]

    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, null=True, verbose_name='Фамилия')
    username = models.CharField(max_length=20, verbose_name='Логин')
    password = models.CharField(max_length=20, verbose_name='Пароль')
    role = models.CharField(max_length=20, choices=ROLE, default='member', verbose_name='Роль')
    age = models.IntegerField(verbose_name='Возраст')
    locations = models.ManyToManyField(Location, verbose_name='Адрес')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ads(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тема')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Автор')
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


class UsersEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Users):
            return {'id': o.id,
                    'username': o.username,
                    'first_name': o.first_name,
                    'last_name': o.last_name,
                    'role': o.role,
                    'age': o.age,
                    'locations': list(o.locations.all().values_list("name", flat=True))}
        return super().default(o)


class AdsEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Ads):
            return {'id': o.id,
                    'name': o.name,
                    'author_id': o.author_id,
                    'author': o.author.first_name,
                    'price': o.price,
                    'description': o.description,
                    'is_published': o.is_published,
                    'image': o.image.url if o.image else None,
                    'category': o.category_id}
        return super().default(o)


class CatEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Categories):
            return {'id': o.id,
                    'name': o.name}
        return super().default(o)

