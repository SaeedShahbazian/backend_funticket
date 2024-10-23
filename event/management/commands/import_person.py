from django.core.management.base import BaseCommand
from django.conf import settings
from event.models import Person
import mysql.connector


class Command(BaseCommand):
    help = "Import Person from MySql"

    def handle(self, *args, **kwargs):
        toto_success = 0
        conn = mysql.connector.connect(
            host=settings.MYSQL_SERVER,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASS,
            database=settings.MYSQL_DB,
            charset=settings.MYSQL_CHARSET,
        )

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * from actor a")
        for row in cursor:
            # TODO Normalizer name (old use hazm)
            full_name = row['name']
            person = Person.objects.filter(legacy_id=row['id']).first()
            if not person:
                person = Person.objects.filter(full_name=full_name).first()
            if not person:
                person = Person(
                    legacy_id=row['id'],
                    full_name=full_name,
                    birthdate=row['birthday'] if row['birthday'] else None,
                )
                person.save()
                if person:
                    toto_success = toto_success + 1

        # Info Command
        print("=====================================")
        print(F"[Info] Total Insert Success: {toto_success}")
