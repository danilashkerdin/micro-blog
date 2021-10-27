from rest_framework import viewsets, generics

from .models import Like
from .serializers import LikeSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all().order_by('id')
    serializer_class = LikeSerializer


class LikeList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
