from rest_framework import serializers


class BaseActivitySerializer(serializers.ModelSerializer):
    """Базовой сериализатор."""

    created_at = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True,
    )
