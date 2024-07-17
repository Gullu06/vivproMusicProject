from django.db import models # type: ignore
from django.contrib.auth.models import User

class Song(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    mode = models.IntegerField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.FloatField()
    time_signature = models.IntegerField()
    num_bars = models.IntegerField()
    num_sections = models.IntegerField()
    num_segments = models.IntegerField()
    rating = models.FloatField(null=True, blank=True)

    def update_star_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.star_rating = average_rating
            self.save()
        else:
            self.star_rating = 0.0
            self.save()

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user.username} rated {self.song.title} - {self.rating}'

class UserSongRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_song_ratings')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='user_song_ratings')

    class Meta:
        unique_together = ('user', 'song')

    def __str__(self):
        return f'{self.user.username} rated {self.song.title}'
