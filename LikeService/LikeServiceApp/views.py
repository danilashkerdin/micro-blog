from rest_framework import viewsets

from .models import Like
from .serializers import LikeSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all().order_by('id')
    serializer_class = LikeSerializer
