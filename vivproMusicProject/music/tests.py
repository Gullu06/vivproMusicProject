from rest_framework.test import APITestCase # type: ignore
from rest_framework import status # type: ignore
from unittest.mock import patch, MagicMock
from .models import Song

class SongViewSetTests(APITestCase):
    def setUp(self):
        # Set up initial test data
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
        response = self.client.get('/api/songs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_song(self):
        response = self.client.get('/api/songs/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Song One')

    def test_filter_by_title(self):
        response = self.client.get('/api/songs/', {'title': 'One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_rate_song(self):
        response = self.client.patch('/api/songs/1/rate/', {'rating': 4.5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4.5)

    def test_invalid_rating(self):
        response = self.client.patch('/api/songs/1/rate/', {'rating': 6})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rating', response.data)
        self.assertEqual(response.data['rating'][0], 'Ensure this value is less than or equal to 5.')

    def test_missing_rating(self):
        response = self.client.patch('/api/songs/1/rate/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['rating'], ['This field is required.'])
