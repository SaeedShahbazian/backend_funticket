from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from comment.models import Thread
from event.models import Event


@receiver(post_save, sender=Event, dispatch_uid="create_event_thread")
def create_event_thread(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: instance.threads.add(Thread.objects.create()))
