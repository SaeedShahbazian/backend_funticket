from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Rate(models.Model):

    EVENT = 'event'
    ACTOR = 'actor'
    RATE_TYPE = (
        (EVENT, _('event')),
        (ACTOR, _('actor')),
    )
    rate = models.FloatField(
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    user = models.ForeignKey(
        User,
        related_name='rates',
        on_delete=models.CASCADE
    )
    rate_type = models.CharField(max_length=10, choices=RATE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
