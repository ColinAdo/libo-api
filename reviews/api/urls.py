from rest_framework.routers import DefaultRouter

from .views import ReviewsViewset

router = DefaultRouter()

router.register(r'reviews', ReviewsViewset, basename='reviews')
urlpatterns = router.urls
