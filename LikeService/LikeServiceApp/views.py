from rest_framework import viewsets, generics

from .models import Like
from .serializers import LikeSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all().order_by('id')
    serializer_class = LikeSerializer


class LikeList(generics.ListCreateAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        queryset = Like.objects.all()
        postID = self.request.query_params.get('postID')
        if postID is not None:
            queryset = queryset.filter(postID=postID)
        return queryset


class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
