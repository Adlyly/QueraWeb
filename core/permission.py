from rest_framework.permissions import BasePermission, SAFE_METHODS  
from userprofile.models import UserProfile

class IsHolderOfCourseOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method == 'POST':
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                return False
            return user_profile.role == 'holder'
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return False
        return user_profile in obj.holders.all()
    
class SubmissionAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_profile = request.user.user
        is_owner = obj.participant == user_profile
        is_holder = obj.course.holders.filter(id=user_profile.id).exists()

        if request.method in SAFE_METHODS:
            return is_owner or is_holder

        if request.method in ['PUT', 'PATCH'] and 'situation' in request.data and not is_owner:
            return True

        return is_owner

class SubmissionSituationEditPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_profile = request.user.user
        if request.method in ['PUT', 'PATCH']:
            if 'situation' in request.data:
                return obj.course.holders.filter(id=user_profile.id).exists()
        return True
    