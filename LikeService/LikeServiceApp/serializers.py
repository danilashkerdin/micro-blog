from rest_framework import serializers

from .models import Like


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'postID', 'userID', 'name')
