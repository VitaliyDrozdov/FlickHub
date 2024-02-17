from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and (request.user.is_admin 
            or request.user.is_staff 
            or request.user.is_superuser)
            )
class IsCurrentUserOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated 

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user
            
