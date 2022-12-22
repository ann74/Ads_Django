from pytest_factoryboy import register

from tests.factories import UserFactory, CategoryFactory, AdFactory

pytest_plugins = "tests.fixtures"

# Factories
register(UserFactory, _name='user')
register(CategoryFactory, _name='categories')
register(AdFactory, _name='ad')
