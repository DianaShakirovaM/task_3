from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import (
    filters,
    mixins,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from activity.models import Action, Follow, Task
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    ActionSerializer,
    FollowSerializer,
    TaskSerializer,
    UpdateUserSerializer,
)

User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ActivityFeedViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('action', 'profile')
    ordering_fields = ('created_at',)

    def get_queryset(self):
        queryset = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from:
            date_from = datetime.strptime(date_from, '%d.%m.%Y').date()
            queryset = queryset.filter(created_at__gte=date_from)

        if date_to:
            date_to = datetime.strptime(date_to, '%d.%m.%Y').date()
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset


class CustomUserViewSet(UserViewSet):

    @action(
        detail=False,
        methods=('put', 'get'),
        permission_classes=(IsAuthenticated,),
        url_name='me'
    )
    def me(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'PUT':
            serializer = UpdateUserSerializer(
                instance=user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id):
        following = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            serializer = FollowSerializer(
                data={'user': request.user.id, 'following': following.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        get_object_or_404(
            Follow, following=following, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
