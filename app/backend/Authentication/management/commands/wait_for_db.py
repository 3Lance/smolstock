import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Command to pause execution until database is available

    Usage:
        python manage.py wait_for_db
    """

    help = 'Pause execution until database is available'

    def handle(self, *args, **options):
        """Function to pause execution until database is available"""
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waititng 1 second...')
                time.sleep(1)

        self.stdout.write(
            self.style.SUCCESS(
                'Database available!'
                )
            )
