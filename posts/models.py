from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    length = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"Post by {self.author.username}"