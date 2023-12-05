from django.core.management.base import BaseCommand
from posts.models import User, Post

class Command(BaseCommand):
    help = 'Initializes the database with predefined users and posts'

    def handle(self, *args, **kwargs):
        users_and_posts = [
            {'username': 'alice', 'password': 'redqueen', 'post_content': 'Curiouser and curiouser!'},
            {'username': 'bob', 'password': 'squarepants', 'post_content': 'I\'m ready, I\'m ready, I\'m ready!'},
            {'username': 'admin', 'password': 'admin', 'is_admin': True, 'post_content': 'Admin reporting in!'}
        ]

        for user_data in users_and_posts:
            user, created = User.objects.get_or_create(
                username=user_data['username'], 
                defaults={'password': user_data['password'], 'is_admin': user_data.get('is_admin', False)}
            )
            if created:
                Post.objects.create(
                    author=user,
                    content=user_data['post_content']
                )

        self.stdout.write(self.style.SUCCESS('Successfully initialized the database with users and posts'))
