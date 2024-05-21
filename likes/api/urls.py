from django.urls import path

from .views import LikeReviewAPIView

urlpatterns = [
    path('like/<int:pk>/', LikeReviewAPIView.as_view(), name='like'),
]
