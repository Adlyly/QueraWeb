from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_premission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)