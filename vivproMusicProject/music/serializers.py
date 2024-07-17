# music/serializers.py
from rest_framework import serializers # type: ignore
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class SongRatingSerializer(serializers.Serializer):
    rating = serializers.FloatField(min_value=0, max_value=5)
