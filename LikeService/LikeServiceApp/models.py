from django.db import models


class Like(models.Model):
    postID = models.PositiveBigIntegerField()
    name = models.CharField(max_length=50)
    userID = models.PositiveBigIntegerField()
