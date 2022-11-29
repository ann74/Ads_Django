import json

from django.core.management import BaseCommand

from ads.models import Ads, Categories
from authentication.models import Location, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('ads\data\\categories.json', encoding='utf-8') as file:
            for item in json.load(file):
                cat = Categories(
                    name=item['name']
                )
                cat.save()

        with open('ads\data\\locations.json', encoding='utf-8') as file:
            for item in json.load(file):
                loc = Location(
                    name=item['name'],
                    lat=item['lat'],
                    lng=item['lng']
                )
                loc.save()

        with open('ads\data\\user.json', encoding='utf-8') as file:
            for item in json.load(file):
                user = User(
                    first_name=item['first_name'],
                    last_name=item['last_name'],
                    username=item['username'],
                    password=item['password'],
                    role=item['role'],
                    age=item['age']
                )
                user.save()
                loc_obj = Location.objects.get(id=item['location_id'])
                user.locations.add(loc_obj)
                user.save()

        with open('ads\data\\ad.json', encoding='utf-8') as file:
            for item in json.load(file):
                ad = Ads(
                    name=item['name'],
                    author=User.objects.get(id=item['author_id']),
                    price=item['price'],
                    description=item['description'],
                    is_published=item['is_published'].title(),
                    image=item['image'],
                    category=Categories.objects.get(id=item['category_id'])
                )
                ad.save()
