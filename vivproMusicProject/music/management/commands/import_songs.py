import json
from django.core.management.base import BaseCommand # type: ignore
from music.models import Song

class Command(BaseCommand):
    help = 'Load songs data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def is_json_valid(self, file_path):
        try:
            with open(file_path, 'r') as file:
                json.load(file)
                return True
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            return False
        except FileNotFoundError:
            print("File not found.")
            return False


    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        if self.is_json_valid(json_file):
            Song.objects.all().delete()
            with open(json_file, 'r') as f:
                data = json.load(f)
                for i in range(len(data['id'])):
                    Song.objects.create(
                    id=data['id'][str(i)],
                    title=data['title'][str(i)],
                    danceability=data['danceability'][str(i)],
                    energy=data['energy'][str(i)],
                    key=data['key'][str(i)],
                    mode=data['mode'][str(i)],
                    acousticness=data['acousticness'][str(i)],
                    instrumentalness=data['instrumentalness'][str(i)],
                    liveness=data['liveness'][str(i)],
                    loudness=data['loudness'][str(i)],
                    valence=data['valence'][str(i)],
                    tempo=data['tempo'][str(i)],
                    duration_ms=data['duration_ms'][str(i)],
                    time_signature=data['time_signature'][str(i)],
                    num_bars=data['num_bars'][str(i)],
                    num_sections=data['num_sections'][str(i)],
                    num_segments=data['num_segments'][str(i)],
                    rating=data.get('rating', None),
                )
                    self.stdout.write(self.style.SUCCESS('Successfully imported songs data'))
