from django.forms import ValidationError
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from core.models import Course, Question, Submission, TestCase
from core.permission import CanCreateSubmission, IsHolderOrParticipantPermission, IsOwnerOrCourseHolder
from core.serializers import CourseCreateUpdateSerializer, CourseSerializer, QuestionCreateSerializer, QuestionSerializer, SubmissionSerializer, TestCaseSerializer, TestCasesCreateSerializer
from userprofile.models import UserProfile

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionCreateSerializer
        return QuestionSerializer

    def perform_create(self, serializer):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        serializer.save(author=user_profile)

    def perform_update(self, serializer):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        if serializer.instance.author != user_profile and self.request.user.is_superuser == 0:
            raise PermissionDenied("You can only update your own questions.")
        serializer.save()

    def perform_destroy(self, instance):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        if instance.author != user_profile and self.request.user.is_superuser == 0:
            raise PermissionDenied("You can only delete your own questions.")
        instance.delete()

class CourseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsHolderOrParticipantPermission]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Course.objects.none()
        
        if user.is_superuser or user.is_staff:
            return Course.objects.all()

        try:
            profile = UserProfile.objects.get(user=user)
        except:
            return Course.objects.none()

        return Course.objects.filter(
            Q(participants=profile) | Q(holders=profile)
        ).distinct()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseSerializer

    
class TestCaseViewSet(ModelViewSet):
    queryset = TestCase.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return TestCasesCreateSerializer
        return TestCaseSerializer

    def perform_create(self, serializer):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        serializer.save(author=user_profile)

    def perform_update(self, serializer):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        if serializer.instance.author != user_profile and self.request.user.is_superuser == 0:
            raise PermissionDenied("You can only update your own testcase.")
        serializer.save()

    def perform_destroy(self, instance):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        if instance.author != user_profile and self.request.user.is_superuser == 0:
            raise PermissionDenied("You can only delete your own testcase.")
        instance.delete()

class SubmissionViewSet(ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, CanCreateSubmission, IsOwnerOrCourseHolder]

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        course_id = self.request.query_params.get("course_id") or self.request.data.get("course")

        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Submission.objects.none()
            
        if self.request.user.is_superuser:
            return Submission.objects.all()

        courses_as_holder = Course.objects.filter(holders=user_profile)
        courses_as_participant = Course.objects.filter(participants=user_profile)

        return Submission.objects.filter(
            Q(course__in=courses_as_holder) | Q(course__in=courses_as_participant, participant=user_profile)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(participant=UserProfile.objects.get(user=self.request.user))

    def perform_update(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        instance = serializer.instance
        old_course = instance.course
        new_course_id = self.request.data.get("course", None)
        if new_course_id:
            try:
                new_course = Course.objects.get(id=new_course_id)
            except Course.DoesNotExist:
                raise PermissionDenied("Invalid course ID.")

            if (
                user_profile not in new_course.participants.all()
                and user_profile not in new_course.holders.all()
                and not self.request.user.is_superuser
            ):
                raise PermissionDenied("Invalid course ID.")

        is_holder = user_profile in old_course.holders.all() or self.request.user.is_superuser
        if not is_holder and 'situation' in self.request.data:
            data = self.request.data.copy()
            data.pop('situation', None)
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer.save()
