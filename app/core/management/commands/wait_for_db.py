import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until db loads"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for DB...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database not available yet...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
