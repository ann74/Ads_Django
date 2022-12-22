import factory

from ads.models import Categories, Ads
from authentication.models import User


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categories

    name = 'Test_category'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    password = '12345'


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ads

    name = 'test_ad'
    description = 'description'
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    price = 500
    is_published = True
