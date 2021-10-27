from django.db import models


class Like(models.Model):
    postID = models.PositiveBigIntegerField()
    userID = models.PositiveBigIntegerField()
