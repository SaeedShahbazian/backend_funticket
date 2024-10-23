from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from comment.models import Thread
from funticket.models import Rate
from media.models import Image, Video
from place.models import Place, PlaceHall
from users.models import User

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
    legacy_id = models.IntegerField(blank=True, null=True,)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    parent = models.ForeignKey(
        'self',
        related_name="category_parent",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    legacy_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Categories"


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
    likes = models.ManyToManyField(
        User,
        related_name='liked_person',
        blank=True
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='disliked_person',
        blank=True
    )
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    telegram_id = models.URLField(
        max_length=200,
        null=True,
        blank=True,
    )
    instagram_id = models.URLField(
        max_length=200,
        null=True,
        blank=True,
    )
    images = models.ManyToManyField(
        Image,
        related_name='image_person',
        blank=True
    )
    biography = models.TextField(blank=True, null=True)
    birthdate = models.DateTimeField(null=True, blank=True)

    legacy_id = models.IntegerField(blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

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
        related_name='genre_event',
        blank=True,
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
    categories = models.ManyToManyField(
        Category,
        related_name='categories_events',
        blank=True
    )
    release_year = models.IntegerField(default=0, blank=True, null=True)
    production_year = models.IntegerField(default=0, blank=True, null=True)
    rules = ArrayField(models.CharField(max_length=50, blank=True, null=True), blank=True, null=True)
    Can_cancel_ticket = models.BooleanField(default=False)
    weight = models.FloatField(null=False, default=0.0)
    event_rate = models.FloatField(default=0)
    rate_sum_cache = models.FloatField(default=0)
    rate_count_cache = models.BigIntegerField(default=0)
    duration = models.IntegerField(null=True, blank=True)
    users_rating = models.FloatField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True,)
    legacy_id = models.IntegerField(blank=True, null=True, unique=True)
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


class HomeActors(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='person_home_actors'
    )
    order = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        ordering = ['order']


class EventSchedule(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_schedule"
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="place_schedule"
    )
    place_hall = models.ForeignKey(
        PlaceHall,
        on_delete=models.CASCADE,
        related_name="place_hall_schedule"
    )
    online_fee = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    vat = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    start_at = models.DateTimeField(
        null=False,
        blank=False
    )
    discount_percent = models.IntegerField(
        null=True,
        blank=True
    )
    discount_amount = models.IntegerField(
        null=True,
        blank=True
    )
    starred_text = models.TextField(
        null=True,
        blank=True
    )
    enable = models.BooleanField(default=True)
    min_price = models.PositiveIntegerField()
    max_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        indexes = [
            models.Index(fields=['event', 'start_at']),
        ]


class ExternalEvent(models.Model):
    GISHE = 'gishe'
    SAMFA = 'samfa'
    DRIVERS = (
        (GISHE, _('Gishe')),
        (SAMFA, _('SAMFA')),
    )
    driver = models.CharField(max_length=5, choices=DRIVERS)
    external_id = models.CharField(max_length=30)
    external_name = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='externals')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        unique_together = [
            ['driver', 'external_id'],
        ]


class ExternalSchedule(models.Model):
    GISHE = 'gishe'
    SAMFA = 'samfa'
    DRIVERS = (
        (GISHE, _('Gishe')),
        (SAMFA, _('SAMFA')),
    )
    driver = models.CharField(max_length=5, choices=DRIVERS)
    external_id = models.CharField(max_length=30)
    external_name = models.CharField(max_length=200)
    schedule = models.ForeignKey(EventSchedule, on_delete=models.PROTECT, related_name='externals')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        unique_together = [
            ['driver', 'external_id'],
        ]
