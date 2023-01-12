import time

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError

from django.core.management import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Waiting for database ...")
        db_ready = False
        while db_ready is False:
            try:
                self.check(databases=["default"])
                db_ready = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write("Database unvailable, waiting 1 second ...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database is available!"))
