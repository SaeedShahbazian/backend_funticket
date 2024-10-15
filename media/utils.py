import base64
import requests
from PIL import Image as PilImage
from django.core import files
from io import BytesIO

from media.models import Image


def url_to_image(url):
    "Convert url image to custom image and save in media"

    response = requests.get(url, stream=True)
    fp = BytesIO()
    fp.write(response.content)
    image = Image()
    image.desktop.save('%s.%s' % (str(image.uuid), PilImage.open(fp).format.lower()), files.File(fp))
    image.save()
    return image


def base64_to_image(base64_str):
    "Convert base64 image to image and save in media"

    for it in ['JPG', 'PNG', 'JPEG', 'GIF']:
        base64_str = base64_str.replace(F"data:image/{it.lower()};base64,", "")
        base64_str = base64_str.replace(F"data:image/{it};base64,", "")

    img_bytes = base64.b64decode(base64_str)
    fp = BytesIO(img_bytes)
    image = Image()
    image.desktop.save('%s.%s' % (str(image.uuid), PilImage.open(fp).format.lower()), files.File(fp))
    image.save()
    return image
