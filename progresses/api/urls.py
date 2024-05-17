from rest_framework.routers import DefaultRouter

from .views import ProgressViewset

route = DefaultRouter()
route.register(r'progress', ProgressViewset, basename='progress')
urlpatterns = route.urls
