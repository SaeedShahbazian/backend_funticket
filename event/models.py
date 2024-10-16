from threading import Thread
from django.db import models

from funticket.models import Rate
from media.models import Image, Video


EVENT_TYPES = (
    ('theater', 'Theater'),
    ('cinema', 'Cinema'),
)


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name


class Person(models.Model):
    full_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    profile_photo = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='persons',
        null=True, blank=True
    )
    birthdate = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.full_name


class Role(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    meta_description = models.TextField(
        blank=True,
        null=True,
    )
    meta_keywords = models.TextField(
        blank=True,
        null=True,
    )
    poster = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='event_poster',
        null=True, blank=True
    )
    aparat_trailer = models.URLField(
        null=True, blank=True
    )
    background = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='event_background',
        null=True, blank=True
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=10,
        choices=EVENT_TYPES,
        null=False,
        blank=False,
        default="theater"
    )
    actors = models.ManyToManyField(
        Person,
        related_name='actors_event',
        blank=True,
        through='EventsActors',
        through_fields=('event', 'person'),
    )
    writers = models.ManyToManyField(
        Person,
        related_name='writers_event',
        blank=True
    )
    directors = models.ManyToManyField(
        Person,
        related_name='directors_event',
        blank=True
    )
    producers = models.ManyToManyField(
        Person,
        related_name='producers_event',
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='genres_event',
        blank=True
    )
    rates = models.ManyToManyField(
        Rate,
        related_name='reate_events',
        blank=True,
    )
    threads = models.ManyToManyField(
        Thread,
        related_name='thread_events',
        blank=True
    )
    images = models.ManyToManyField(
        Image,
        related_name='image_events',
        blank=True
    )
    videos = models.ManyToManyField(
        Video,
        related_name='video_events',
        blank=True
    )

    weight = models.FloatField(null=False, default=0.0)
    event_rate = models.FloatField(default=0)
    rate_sum_cache = models.FloatField(default=0)
    rate_count_cache = models.BigIntegerField(default=0)
    duration = models.IntegerField(null=True, blank=True)
    users_rating = models.FloatField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.name


class EventsActors(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_actors'

    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='person_event_actors'
    )
    order = models.IntegerField(default=1000)

    class Meta:
        ordering = ['order']


class EventRole(models.Model):
    role = models.ForeignKey(
        Role,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='roles_event'
    )
    person = models.ForeignKey(
        Person,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='person_roles_event'
    )
    event = models.ForeignKey(
        Event,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='event_roles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
