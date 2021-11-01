from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    userID = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
