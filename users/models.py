from django.db import models
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
# from PIL import Image as PilImage
from django.contrib.auth.models import AbstractUser
from users.utils import generate_random_username

from geo.models import City
from media.models import Image


class User(AbstractUser):
    FEMALE = 'f'
    MALE = 'm'
    GENDER = [
        (FEMALE, _('Female')),
        (MALE, _('Male'))
    ]
    full_name = models.CharField(_('full name'), max_length=150)
    phone_number = models.CharField(
        _('phone number'), max_length=12, blank=True,
        unique=True,
    )
    username = models.CharField(
        max_length=32,
        unique=True,
        default=generate_random_username,
    )
    gender = models.CharField(
        choices=GENDER,
        max_length=1,
        null=True,
    )
    email = models.EmailField(unique=False, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    REQUIRED_FIELDS = ['phone_number']
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="user_city"
    )
    avatar = ResizedImageField(
        size=[300, 300],
        crop=['middle', 'center'],
        null=True, blank=True,
        upload_to='image/avatars',
    )

    def get_full_name(self):
        """
        Return the full_name
        """
        return self.full_name.strip()

    @classmethod
    def find(cls, id):
        result = cls.objects.filter(id=id)
        return result.first()

    @classmethod
    def list(cls, data):
        query = {}

        if 'phone_number' in data:
            data['phone_number'] = data['phone_number'].replace('+', '')
            query['phone_number__icontains'] = data['phone_number']

        if 'email' in data:
            query['email__icontains'] = data['email']

        if 'full_name' in data:
            query['full_name__icontains'] = data['full_name']

        order = data['sort_by']

        if data['order'] == 'desc':
            order = '-' + order

        qry = cls.objects.filter(
            **query
        )
        if 'groups' in data:
            for item in data['groups']:
                qry = qry.filter(groups__name__in=[item])

        return qry.order_by(order)


class Message(models.Model):
    user = models.ForeignKey(
        User,
        related_name="messages",
        on_delete=models.PROTECT
    )
    title = models.CharField(max_length=400)
    message_content = models.TextField()
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True, blank=True
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    message_sender = models.ForeignKey(
        User,
        related_name="message_senders",
        on_delete=models.PROTECT
    )
