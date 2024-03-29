from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """
    Разрешает доступ только администраторам
    и сотрудникам административной части.
    """

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrUserOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только администраторам и авторизованным пользователям.
    Чтение доступно всем пользователям.

    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsAdminOrModeratorOrAuthorOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Разрешает доступ только администраторам, модераторам и авторам для
    конкретного объекта. Чтение доступно всем пользователям.

    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
