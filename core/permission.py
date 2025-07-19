from rest_framework.permissions import BasePermission, SAFE_METHODS  
from userprofile.models import UserProfile

class IsHolderOrParticipantPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        try:
            profile = UserProfile.objects.get(user=user)
        except:
            return False
        if request.method in SAFE_METHODS:
            return profile in obj.participants.all() or profile in obj.holders.all() or user.is_superuser
        return profile in obj.holders.all() or user.is_superuser



    
# class SubmissionAccessPermission(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         user_profile = request.user.user
#         is_owner = obj.participant == user_profile
#         is_holder = obj.course.holders.filter(id=user_profile.id).exists()

#         if request.method in SAFE_METHODS:
#             return is_owner or is_holder

#         if request.method in ['PUT', 'PATCH'] and 'situation' in request.data and not is_owner:
#             return True

#         return is_owner

# class SubmissionSituationEditPermission(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         user_profile = request.user.user
#         if request.method in ['PUT', 'PATCH']:
#             if 'situation' in request.data:
#                 return obj.course.holders.filter(id=user_profile.id).exists()
#         return True
    