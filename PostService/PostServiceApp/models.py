from django.db import models


class Post(models.Model):
    header = models.CharField(max_length=20)
    text = models.CharField(max_length=500)
    userID = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
