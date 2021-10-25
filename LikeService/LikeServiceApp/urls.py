from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'likes', views.LikeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view()),
]
