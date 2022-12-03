from django.core.management import BaseCommand

from authentication.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

