from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from media.models import Image
from geo.models import City
from comment.models import Thread
from users.models import User


FACILITIES_TYPES = (
    ('elevator', 'Elevator'),
    ('parking', 'Parking'),
    ('buffet', 'Buffet'),
    ('restaurant', 'Restaurant'),
    ('carwash', 'Carwash'),
    ('card_reader', 'CardReader'),
    ('print_ticket', 'PrintTicket'),
    ('disabled_access', 'DisabledAccess'),
    ('atm', 'ATM'),
    ('coffee_shop', 'CoffeeShop'),
    ('book_shop', 'BookShop'),
    ('foodcourt', 'FoodCourt'),
    ('internet', 'Internet'),
)

STATUS_TYPES = (
    ('theatr', 'Theater'),
    ('close', 'Close'),
    ('repairing', 'Repairing'),
    ('multidimentional', 'Multidimentional'),
    ('preparing', 'Preparing'),
    ('non-mechanized', 'Nonmechanized'),
    ('active', 'Active')
)


class Place(models.Model):
    thumbnail = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='place_thumbnail',
        null=True, blank=True
    )
    name_fa = models.CharField(
        max_length=100,
        null=False, blank=False
    )
    name_en = models.CharField(
        max_length=100,
        null=True, blank=True
    )
    manager = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    place_code = models.IntegerField(
        null=True,
        default=None
    )
    rate = models.FloatField(default=0)
    rate_count = models.BigIntegerField(default=0)
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
    facility = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            choices=FACILITIES_TYPES
        ),
        default=list,
        null=True,
        blank=True
    )
    halls_count = models.IntegerField(
        null=True,
        blank=True,
        default=0
    )
    seats_count = models.IntegerField(
        default=0
    )
    gishe_count = models.IntegerField(
        default=0
    )
    kiosk_count = models.IntegerField(
        default=0
    )
    description = models.TextField(
        max_length=5000,
        null=True, blank=True
    )
    address = models.CharField(
        max_length=2000,
        null=True, blank=True
    )
    access_description = models.CharField(
        max_length=2000,
        null=True,
        blank=True
    )
    telephone = ArrayField(
        models.CharField(
            max_length=20,
            blank=True,
        ),
        default=list,
        null=True,
        blank=True
    )
    sales_capacity = models.IntegerField(
        null=False,
        default=10
    )

    location = models.PointField(
        null=True,
        blank=True
    )

    verified = models.BooleanField(default=False)

    established_at = models.DateTimeField(
        null=True,
        blank=True
    )
    renovated_at = models.DateTimeField(
        null=True,
        blank=True
    )
    # TODO
    # contracts = models.ManyToManyField(Contract, related_name="cinemas", default=list, blank=True)
    threads = models.ManyToManyField(
        Thread,
        related_name='thread_places',
        blank=True
    )
    weight = models.FloatField(
        null=False,
        default=0
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name='places',
        null=True, blank=True
    )
    online_fee = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    vat = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    rules = ArrayField(models.CharField(max_length=50, blank=True, null=True), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    @classmethod
    def find(cls, idx):
        return cls.objects.filter(id=idx).first()

    @classmethod
    def list(cls, data):
        query = {}
        if 'facilities' in data:
            query['facility__in'] = data['facilities']

        result = cls.objects.filter(
            **query
        )

        if 'name' in data:
            result = result.filter(
                Q(name_fa__icontains=data['name']) | Q(name_en__icontains=data['name'])
            )

        return result.all()

    def __str__(self):
        return self.name_fa


class PlaceHall(models.Model):
    name = models.CharField(
        max_length=100,
        null=False, blank=False
    )
    place = models.ForeignKey(
        Place,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='halls'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    @classmethod
    def list(cls, data):
        query = {}
        if 'place_id' in data:
            query['place__id'] = data['place_id']

        result = cls.objects.filter(
            **query
        )

        return result.all()


# class Ticket(models.Model):
#     AVAILABLE = 'av'
#     SOLD = 'so'
#     RESERVED = 'res'
#     STATUS = (
#         (AVAILABLE, _('Available')),
#         (SOLD, _('Sold')),
#         (RESERVED, _('Reserved')),
#     )
#     GISHE = 'gishe'
#     SAMFA = 'samfa'
#     DRIVER = (
#         (GISHE, _('Gishe')),
#         (SAMFA, _('SAMFA')),
#     )
#     status = models.CharField(choices=STATUS, max_length=4, default=AVAILABLE)
#     price = models.BigIntegerField()
#     user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='tickets')
#     basket = models.ForeignKey('payment.Basket', on_delete=models.PROTECT, related_name='tickets')
#     driver = models.CharField(choices=DRIVER, max_length=10)
#     expire_at = models.DateTimeField(null=True, blank=True)
#     movie = models.ForeignKey('event.Event', on_delete=models.PROTECT, related_name='tickets')
#     session = models.ForeignKey('event.EventSchedule', on_delete=models.PROTECT, related_name='tickets')
#     seat_id = models.CharField(max_length=32)
#     seat_row = models.CharField(max_length=32)
#     seat_number = models.CharField(max_length=32)
#     reserve_code = models.CharField(max_length=32)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

#     class Meta:
#         unique_together = [['session', 'seat_id']]
