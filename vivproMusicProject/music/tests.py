from unittest.mock import patch
from rest_framework import status # type: ignore
from rest_framework.test import APITestCase # type: ignore
from django.urls import reverse # type: ignore
from .models import Rating, Song, UserSongRating
from django.contrib.auth.models import User # type: ignore

class SongViewSetTests(APITestCase):
    def setUp(self):
        self.song1 = Song.objects.create(
            id='1', title='Song One', danceability=0.5, energy=0.5, key=1, mode=1,
            acousticness=0.5, instrumentalness=0.5, liveness=0.5, loudness=0.5,
            valence=0.5, tempo=120.0, duration_ms=200000, time_signature=4,
            num_bars=16, num_sections=8, num_segments=4, rating=None
        )
        self.song2 = Song.objects.create(
            id='2', title='Song Two', danceability=0.6, energy=0.6, key=2, mode=0,
            acousticness=0.4, instrumentalness=0.4, liveness=0.6, loudness=0.6,
            valence=0.6, tempo=130.0, duration_ms=210000, time_signature=4,
            num_bars=20, num_sections=10, num_segments=5, rating=None
        )

    def test_list_songs(self):
        url = reverse('song-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_song(self):
        url = reverse('song-detail', args=[self.song1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.song1.title)

    def test_retrieve_song_by_title(self):
        url = reverse('song-list')
        response = self.client.get(url, {'title': 'One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        self.assertEqual(response.data['results'][0]['title'], 'Song One')

    def test_rate_song(self):
        url = reverse('song-rate-song', args=[self.song1.id])
        response = self.client.patch(url, {'rating': 4})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4)
        self.song1.refresh_from_db()
        self.assertEqual(self.song1.rating, 4)

    def test_invalid_rating(self):
        url = reverse('song-rate-song', args=[self.song1.id])
        response = self.client.patch(url, {'rating': 6})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rating', response.data)
        self.assertEqual(response.data['rating'][0], 'Ensure this value is less than or equal to 5.')

    def test_missing_rating(self):
        url = reverse('song-rate-song', args=[self.song1.id])
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rating', response.data)

    def test_get_rating(self):
        self.song1.rating = 3
        self.song1.save()
        url = reverse('song-rate-song', args=[self.song1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 3)

class RatingTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.song = Song.objects.create(
            id='1', title='Imagine', danceability=0.5, energy=0.5, key=1, mode=1,
            acousticness=0.5, instrumentalness=0.5, liveness=0.5, loudness=0.5,
            valence=0.5, tempo=120.0, duration_ms=200000, time_signature=4,
            num_bars=16, num_sections=8, num_segments=4, rating=None
        )
        self.client.login(username='testuser1', password='testpassword')

    @patch('music.models.Rating.objects.create')
    @patch('music.models.Song.objects.filter')
    @patch('music.models.UserSongRating.objects.create')
    def test_create_rating(self, mock_usersongrating_create, mock_song_filter, mock_rating_create):
        mock_song_filter.return_value.first.return_value = self.song
        mock_rating_create.return_value = Rating(user=self.user1, song=self.song, rating=5)
        mock_usersongrating_create.return_value = UserSongRating(user=self.user1, song=self.song)

        url = reverse('rating-list')
        response = self.client.post(url, {'title': 'Imagine', 'rating': 5, 'user': 1, 'song': "1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_rating_create.assert_called_once_with(user=self.user1, song=self.song, rating=5)
        mock_usersongrating_create.assert_called_once_with(user=self.user1, song=self.song)

    @patch('music.models.UserSongRating.objects.filter')
    @patch('music.models.Song.objects.filter')
    def test_user_cannot_rate_song_twice(self, mock_song_filter, mock_usersongrating_filter):
        mock_song_filter.return_value.first.return_value = self.song
        mock_usersongrating_filter.return_value.exists.return_value = True

        url = reverse('rating-list')
        response = self.client.post(url, {'title': 'Imagine', 'rating': 5, 'user': 1, 'song': "1"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['rating'][0], 'You can only rate a song once.')
        mock_usersongrating_filter.assert_called_once_with(user=self.user1, song=self.song)

    @patch('music.models.UserSongRating.objects.create')
    @patch('music.models.Song.objects.filter')
    @patch('music.models.Rating.objects.create')
    def test_different_users_can_rate_same_song(self, mock_rating_create, mock_song_filter, mock_usersongrating_create):
        mock_song_filter.return_value.first.return_value = self.song
        mock_rating_create.side_effect = [
            Rating(user=self.user1, song=self.song, rating=5),
            Rating(user=self.user2, song=self.song, rating=4)
        ]
        mock_usersongrating_create.side_effect = [
            UserSongRating(user=self.user1, song=self.song),
            UserSongRating(user=self.user2, song=self.song)
        ]

        url = reverse('rating-list')
        self.client.login(username='testuser1', password='testpassword')
        response1 = self.client.post(url, {'title': 'Imagine', 'rating': 5, 'user': 1, 'song': "1"})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.client.login(username='testuser2', password='testpassword')
        response2 = self.client.post(url, {'title': 'Imagine', 'rating': 4, 'user': 2, 'song': "1"})
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
