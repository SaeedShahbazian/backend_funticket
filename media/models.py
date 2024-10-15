import uuid
from django.contrib.gis.db import models
from django.utils import timezone
from PIL import Image as PilImage


def image_directory_path(instance, filename, tp):
    try:
        f = PilImage.open(instance.desktop).format.lower()
    except:
        f = filename.split('.')[-1].lower()
        if not f.upper() in ['PNG', 'JPG', 'GIF', 'JPEG']:
            f = 'jpg'

    now = timezone.now()
    return 'image/{}/{}/{}_{}.{}'.format(now.year, now.month, str(instance.uuid), tp, f)


def desktop_image_directory_path(instance, filename):
    return image_directory_path(instance, filename, 'desktop')


def mobile_image_directory_path(instance, filename):
    return image_directory_path(instance, filename, 'mobile')


class Image(models.Model):

    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    desktop = models.ImageField(
        null=False, blank=False,
        upload_to=desktop_image_directory_path,
    )
    desktop_url = models.URLField(
        null=True, blank=True
    )
    mobile = models.ImageField(
        null=True, blank=True,
        upload_to=mobile_image_directory_path
    )
    mobile_url = models.URLField(
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)


def video_directory_path(instance, filename, tp):
    try:
        f = filename.split('.')[-1]
    except:
        f = 'mp4'
    now = timezone.now()
    return 'video/{}/{}/{}_{}.{}'.format(now.year, now.month, str(instance.uuid), tp, f)


def desktop_video_directory_path(instance, filename):
    return video_directory_path(instance, filename, 'desktop')


def mobile_video_directory_path(instance, filename):
    return video_directory_path(instance, filename, 'mobile')


class Video(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    desktop = models.FileField(
        null=False, blank=False,
        upload_to=desktop_video_directory_path,
    )
    desktop_url = models.URLField(
        null=True, blank=True
    )
    mobile = models.FileField(
        null=True, blank=True,
        upload_to=mobile_video_directory_path,
    )
    mobile_url = models.URLField(
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)


