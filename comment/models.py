from django.utils.translation import gettext_lazy as _
from django.db import models
from users.models import User

THREAD_STATES = (
    ('normal', 'Normal'),
    ('read_only', 'Read Only'),
    ('hidden', 'Hidden'),
)

THREAD_TYPES = (
    ('comment', 'Comment'),
)


class Thread(models.Model):
    type = models.CharField(
        max_length=10,
        choices=THREAD_TYPES,
        default='comment'
    )
    state = models.CharField(
        max_length=10,
        choices=THREAD_STATES,
        default='normal'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)


class Comment(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    COMMENT_STATES = (
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
    )
    user = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
        null=True
    )
    text = models.CharField(
        max_length=1000,
        null=False,
        blank=False
    )
    parent = models.ForeignKey(
        'self',
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    thread = models.ForeignKey(
        Thread,
        related_name="comments",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    state = models.CharField(
        max_length=15,
        choices=COMMENT_STATES,
        default='pending'
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviewed_comments",
        null=True,
        blank=True
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_comments',
        blank=True
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='disliked_comments',
        blank=True
    )
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)

    # TODO     @classmethod
    # TODO  def list(cls, data):
