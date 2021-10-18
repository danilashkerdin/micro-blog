from django.db import models


class Like(models.Model):
    postID = models.PositiveBigIntegerField()
    userID = models.PositiveBigIntegerField()

    def __int__(self):
        return self.postID

    # TODO: If like exists, delete it

# class Hero(models.Model):
#     name = models.CharField(max_length=60)
#     alias = models.CharField(max_length=60)
