from django.db import models


class Comment(models.Model):
    userID = models.IntegerField()
    postID = models.IntegerField()
    text = models.CharField(max_length=100)
