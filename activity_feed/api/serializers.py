from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from activity.models import Action, Follow, Task
from .base_serializers import BaseActivitySerializer
from .fields import Base64Field

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class TaskSerializer(BaseActivitySerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class ActionSerializer(BaseActivitySerializer):
    created_at = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        read_only=True,
    )

    class Meta:
        model = Action
        fields = ('description', 'action', 'created_at')


class UpdateUserSerializer(serializers.ModelSerializer):
    avatar = Base64Field()

    class Meta:
        model = User
        fields = ('avatar', 'bio')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписываться на себя!',
                code='invalid_subscription'
            )
        return value
