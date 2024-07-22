from rest_framework import viewsets, status # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from .models import Rating, Song
from .serializers import SongRatingSerializer, SongSerializer, RatingSerializer
from music.service import SongService
from music import models
from django.contrib.auth.models import User # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        title = self.request.query_params.get('title', None)
        mode = self.request.query_params.get('mode', None)
        service = SongService()
        if title:
            return service.get_songs_by_title(title)
        if mode:
            return service.get_songs_by_mode(mode)
        return service.get_all_songs()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if not serializer.data:
                return Response({'detail': 'No data available.'}, status=status.HTTP_404_NOT_FOUND)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        if not serializer.data:
            return Response({'detail': 'No data available.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'patch'], url_path='rate')
    def rate_song(self, request, pk=None):
        song = self.get_object()

        if request.method == 'GET':
            return Response({'rating': song.rating}, status=status.HTTP_200_OK)

        serializer = SongRatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.validated_data.get('rating')
            if 0 <= rating <= 5:
                song.rating = rating
                song.save()
                return Response({'status': 'rating set', 'rating': rating}, status=status.HTTP_200_OK)
            return Response({"error": "Rating must be between 0 and 5."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = serializer.validated_data.get('user', self.request.user)
        if not self.request.user.is_superuser:
            user = self.request.user
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            rating = serializer.validated_data.get('rating')
            if 0 > rating > 5:
                return Response({"error": "Rating must be between 0 and 5."}, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"rating": "You can only rate a song once."}, status=status.HTTP_400_BAD_REQUEST)
