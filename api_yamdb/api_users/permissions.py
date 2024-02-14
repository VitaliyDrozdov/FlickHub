from rest_framework import permissions

class IsAdminOnly(permissions.BasePermission):
    """
    Пользователи с ролью администратора имеют полный доступ.
    """
    def has_permission(self, request, view):
        # Только администраторы могут выполнять другие действия
        return request.user.role == 'admin'
