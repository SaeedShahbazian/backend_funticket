from django.core.management.base import BaseCommand
from django.conf import settings
from event.models import Genre
import mysql.connector


class Command(BaseCommand):
    help = "Import Genre from MySql"

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
        cursor.execute("SELECT * FROM genre x")
        for row in cursor:
            title = str(row['title']).strip()
            genre = Genre.objects.filter(legacy_id=row['id']).first()

            if not genre:
                genre = Genre(
                    legacy_id=row['id'],
                    name=title,
                )
                genre.save()
                toto_success = toto_success + 1

        # Info Command
        print("=====================================")
        print(F"[Info] Total Insert Success: {toto_success}")
