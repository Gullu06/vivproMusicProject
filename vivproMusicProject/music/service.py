from music.models import Song

class SongService:
    def get_songs_by_title(self, title):
        return Song.objects.filter(title__icontains=title)

    def get_songs_by_mode(self, mode):
        return Song.objects.filter(mode=mode)

    def get_all_songs(self):
        return Song.objects.all()

    def get_song_by_id(self, song_id):
        return Song.objects.filter(id=song_id).first()

    def rate_song(self, song, rating):
        if 0 <= float(rating) <= 5:
            song.rating = rating
            song.save()
            return song
        raise ValueError("Rating must be between 0 and 5.")
