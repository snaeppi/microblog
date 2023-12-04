from django.core.management.base import BaseCommand
from posts.models import User

class Command(BaseCommand):
    help = 'Initializes the database with predefined users'

    def handle(self, *args, **kwargs):
        # Create normal users
        User.objects.get_or_create(username='alice', defaults={'password': 'redqueen'})
        User.objects.get_or_create(username='bob', defaults={'password': 'squarepants'})

        # Create an admin user
        User.objects.get_or_create(username='admin', defaults={'password': 'admin', 'is_admin': True})

        self.stdout.write(self.style.SUCCESS('Successfully created users'))