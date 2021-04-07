from django.db import models


class Post(models.Model):
    text = models.TextField(max_length=150)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)