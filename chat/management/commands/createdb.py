from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Creates SQLite database, runs migrations, and loads data from a JSON dump.'

    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')
        call_command('loaddata', 'dump.json')