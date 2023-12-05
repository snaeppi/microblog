from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from posts.models import Post

class Command(BaseCommand):
    help = 'Initializes the database with predefined users and posts'

    def handle(self, *args, **kwargs):
        users_and_posts = [
            {'username': 'alice', 'password': 'redqueen', 'post_content': 'Curiouser and curiouser!'},
            {'username': 'bob', 'password': 'squarepants', 'post_content': 'I\'m ready, I\'m ready, I\'m ready!'},
            {'username': 'admin', 'password': 'admin', 'email': 'admin@admin.com', 'is_admin': True, 'post_content': 'Admin reporting in!'}
        ]

        for user_data in users_and_posts:
            if not User.objects.filter(username=user_data['username']).exists():
                if 'is_admin' in user_data and user_data['is_admin']:
                    user = User.objects.create_superuser(
                        user_data['username'],
                        email=user_data.get('email', ''),
                        password=user_data['password']
                    )
                else:
                    user = User.objects.create_user(
                        user_data['username'],
                        password=user_data['password']
                    )

                Post.objects.create(
                    author=user,
                    content=user_data['post_content'],
                    length=len(user_data['post_content'])
                )

        self.stdout.write(self.style.SUCCESS('Successfully initialized the database with users and posts'))
        