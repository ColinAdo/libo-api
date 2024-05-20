from django.urls import path

from .views import FavouriteView

urlpatterns = [
    path('favourite/<int:pk>/', FavouriteView.as_view(), name='favourite'),
]