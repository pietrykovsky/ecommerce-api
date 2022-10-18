from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'You are not allowed to do this.'

    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS or request.user and request.user.is_staff):
            return True
        
        return False