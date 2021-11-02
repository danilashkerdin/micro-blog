from django.db import models


class Comment(models.Model):
    userID = models.IntegerField()
    postID = models.IntegerField()
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=100)
