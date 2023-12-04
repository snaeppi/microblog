from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # Flaw: plain text password
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    length = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"Post by {self.author.username}"