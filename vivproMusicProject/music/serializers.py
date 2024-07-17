from rest_framework import serializers # type: ignore
from .models import Rating, Song, UserSongRating

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class SongRatingSerializer(serializers.Serializer):
    rating = serializers.FloatField(min_value=0, max_value=5)

class RatingSerializer(serializers.ModelSerializer):
    title = serializers.CharField(write_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

    def validate(self, data):
        title = data.get('title')
        user = self.context['request'].user

        # Check if the song exists
        song = Song.objects.filter(title__iexact=title).first()
        if not song:
            raise serializers.ValidationError({'title': 'Song not found'})

        if UserSongRating.objects.filter(user=user, song=song).exists():
            raise serializers.ValidationError({'rating': 'You can only rate a song once.'})

        data['song'] = song
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        song = validated_data.pop('song')
        rating = validated_data.pop('rating')

        rating_instance = Rating.objects.create(user=user, song=song, rating=rating)

        UserSongRating.objects.create(user=user, song=song)

        return rating_instance
