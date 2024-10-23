from django.core.management.base import BaseCommand
from django.conf import settings
from event.models import Category
import mysql.connector


class Command(BaseCommand):
    help = "Import Category from MySql"

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
        cursor.execute("SELECT * FROM category x")
        for row in cursor:
            title = str(row['title']).strip()
            category = Category.objects.filter(legacy_id=row['id']).first()

            if not category:
                category = Category(
                    legacy_id=row['id'],
                    name=title,
                )
                category.save()
                toto_success = toto_success + 1

        # Info Command
        print("=====================================")
        print(F"[Info] Total Insert Success: {toto_success}")
