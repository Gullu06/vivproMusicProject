from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from music.views import SongViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'api/songs', SongViewSet)
router.register(r'api/ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
