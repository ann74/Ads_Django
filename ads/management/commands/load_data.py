import json

from django.core.management import BaseCommand

from ads.models import Ads, Categories


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('ads\data\\ads.json', encoding='utf-8') as file:
            for item in json.load(file):
                ad = Ads(
                    name=item['name'],
                    author=item['author'],
                    price=item['price'],
                    description=item['description'],
                    address=item['address'],
                    is_published=item['is_published'].title()
                )
                ad.save()
        with open('ads\data\categories.json', encoding='utf-8') as file:
            for item in json.load(file):
                category = Categories(
                    name=item['name'],
                )
                category.save()
