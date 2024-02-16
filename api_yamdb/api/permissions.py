from rest_framework.permissions import BasePermission, SAFE_METHODS


# based permisson class for Admin, could be changed
class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
        )

    # def has_object_permission(self, request, view, obj):
    #    return request.method == "GET" or request.user.is_admin
