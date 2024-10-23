from django.core.management.base import BaseCommand
from django.conf import settings
from event.models import Event, Genre, Person
import mysql.connector


class Command(BaseCommand):
    help = "Import Event from MySql"

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
        cursor.execute("SELECT eg.genre_ids,e.* from event e \
                       left join (SELECT GROUP_CONCAT(genre_id) as genre_ids,event_id from event_genre group by event_id ) eg \
                       ON eg.event_id = e.id"
                       )
        for row in cursor:

            event = Event.objects.filter(legacy_id=row['id'])
            if event:
                print('exists')
                continue

            event = Event.objects.create(
                name=row['title'],
                meta_title=row['seo_title'],
                meta_description=row['seo_desc'],
                meta_keywords=row['title'],
                description=row['description'],
                # type=row['title'],
                # duration=row['title'],
                release_year=row['production_date'],  # TODO check date or only year
                production_year=row['production_date'],
                legacy_id=row['id']

            )

            # Add directprs
            director_name = str(row['directors']).strip()
            if row['directors'] and director_name != '':
                person = Person.objects.filter(full_name=director_name).first()
                if not person:
                    person = Person(
                        full_name=director_name,
                    )
                    person.save()
                event.directors.add(person)

            # Add producer
            producer_name = str(row['producers']).strip()
            if row['producers'] and producer_name != '':
                person = Person.objects.filter(full_name=producer_name).first()
                if not person:
                    person = Person(
                        full_name=producer_name,
                    )
                    person.save()
                event.producers.add(person)

            # Add genre
            genre_ids = str(row['genre_ids']).split(',')
            if row['genre_ids'] and genre_ids != '':
                genres = Genre.objects.filter(legacy_id__in=genre_ids).all()
                if genres:
                    event.genres.add(*genres)

            toto_success = toto_success + 1

        # Info Command
        print("=====================================")
        print(F"[Info] Total Insert Success: {toto_success}")
