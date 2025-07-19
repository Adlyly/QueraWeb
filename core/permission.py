from rest_framework.permissions import BasePermission, SAFE_METHODS  
from core.models import Course
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



class IsOwnerOrCourseHolder(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_profile = UserProfile.objects.get(user=request.user)
        course_id = request.data.get('course')
        course = Course.objects.get(id=course_id)
        is_participant = obj.participant == user_profile
        is_holder = user_profile in course.holders.all()

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant or is_holder
        return True

class CanCreateSubmission(BasePermission):
    def has_permission(self, request, view):
        if request.method != ['POST', 'PUT']:
            return True

        user_profile = UserProfile.objects.get(user=request.user)
        course_id = request.data.get('course')

        if not course_id:
            return False

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return False

        return user_profile in course.participants.all() or user_profile in course.holders.all() or request.user.is_superuser