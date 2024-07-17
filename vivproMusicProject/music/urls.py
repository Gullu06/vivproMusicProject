from django.urls import include, path # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from .views import SongViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
