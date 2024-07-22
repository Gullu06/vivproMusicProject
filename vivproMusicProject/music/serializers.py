from rest_framework import serializers # type: ignore
from .models import Rating, Song, UserSongRating
from django.contrib.auth.models import User # type: ignore

class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = '__all__'

class SongRatingSerializer(serializers.Serializer):
    rating = serializers.FloatField(min_value=0, max_value=5)

class RatingSerializer(serializers.ModelSerializer):

    title = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Rating
        fields = ['title', 'rating', 'user']

    def validate(self, data):
        title = data.get('title')
        user = data.get('user', self.context['request'].user)

        # Check if the song exists
        song = Song.objects.filter(title__iexact=title).first()
        if not song:
            raise serializers.ValidationError({'title': 'Song not found'})

        # Check if the user has already rated this song
        if UserSongRating.objects.filter(user=user, song=song).exists():
            raise serializers.ValidationError({'rating': 'You can only rate a song once.'})

        data['song'] = song
        return data

    def create(self, validated_data):
        user = validated_data.get('user', self.context['request'].user)
        song = validated_data.pop('song')
        rating = validated_data.pop('rating')

        # Create the rating and UserSongRating objects
        rating_instance = Rating.objects.create(user=user, song=song, rating=rating)
        UserSongRating.objects.create(user=user, song=song)

        return rating_instance
