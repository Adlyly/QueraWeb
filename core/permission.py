from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsHolderOfCourseOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'userprofile') and 
            request.user.userprofile.role == 'holder'
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user_profile = getattr(request.user, 'userprofile', None)
        if not user_profile or user_profile.role != 'holder':
            return False
        return obj.holders.filter(id=user_profile.id).exists()
