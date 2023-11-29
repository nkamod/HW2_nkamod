import json
from django.core.management.base import BaseCommand
from movie_theater_booking.models import Show, Movie

class Command(BaseCommand):
    help = 'Load a list of shows from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file to load data from')
    
    def handle(self, *args, **options):
      # Clear the table
      Show.objects.all().delete()
      self.stdout.write('All shows deleted.')
    
      # Load data from JSON
      with open(options['json_file'], 'r') as file:
          data = json.load(file)
          for entry in data:
              show_data = entry['fields']
    
              # Fetch the Movie instance
              if 'movie' in show_data:
                  try:
                      movie_instance = Movie.objects.get(pk=show_data['movie'])
                      show_data['movie'] = movie_instance
                  except Movie.DoesNotExist:
                      self.stdout.write(f'Movie with id {show_data["movie"]} does not exist.')
                      continue
    
              Show.objects.create(**show_data)
          self.stdout.write(f'{len(data)} shows loaded into the database.')