from django.db import models


class Comment(models.Model):
    userID = models.IntegerField()
    name = models.CharField(max_length=50)
    postID = models.IntegerField()
    text = models.CharField(max_length=100)
