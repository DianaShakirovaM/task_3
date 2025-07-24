from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, SAFE_METHODS
)


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Проверка прав автора."""

    def has_object_permission(self, request, view, task):
        return (
            request.method in SAFE_METHODS or request.user == task.author
        )
