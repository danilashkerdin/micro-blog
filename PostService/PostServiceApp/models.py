from django.db import models


class Post(models.Model):
    text = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    userID = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
