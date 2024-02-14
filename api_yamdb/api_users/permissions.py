from rest_framework import permissions

class IsAdminOnly(permissions.BasePermission):
    """
    Пользователи с ролью администратора имеют полный доступ.
    """
    def has_permission(self, request, view):
        # Разрешаем GET, HEAD или OPTIONS запросы для всех пользователей
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # Только администраторы могут выполнять другие действия
        return request.user.role == 'admin'


class IsMeOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username