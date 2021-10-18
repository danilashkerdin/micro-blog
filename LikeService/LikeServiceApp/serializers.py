from rest_framework import serializers

from .models import Like


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'postID', 'userID')

# from .models import Hero
# class HeroSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Hero
#         fields = ('id', 'name', 'alias')
