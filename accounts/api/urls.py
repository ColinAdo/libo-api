from django.urls import path

from .views import ProfileView

urlpatterns = [
    path('profile/<str:profId>/', ProfileView.as_view(), name='profile'),
]

