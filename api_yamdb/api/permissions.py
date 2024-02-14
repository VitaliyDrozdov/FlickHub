from rest_framework import permissions


# based permisson class for Admin, could be changed
class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return request.user.role == 'admin'
