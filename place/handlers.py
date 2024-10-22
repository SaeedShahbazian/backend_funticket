from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from comment.models import Thread
from place.models import Place


@receiver(post_save, sender=Place, dispatch_uid="create_place_thread")
def create_place_thread(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: instance.threads.add(Thread.objects.create()))
