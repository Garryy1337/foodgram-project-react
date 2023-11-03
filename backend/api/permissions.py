from rest_framework import permissions


class IsAdminAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    message = "Доступ запрещен!"

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or obj.author == request.user
        )
