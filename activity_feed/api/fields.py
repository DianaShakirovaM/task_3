import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64Field(serializers.ImageField):
    """Кодирует/декодирует фото."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64',)
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
        return super().to_internal_value(data)
