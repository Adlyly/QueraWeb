from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from core.models import Course, Question, Submission, TestCase
from core.permission import IsHolderOrParticipantPermission
from core.serializers import CourseCreateUpdateSerializer, CourseSerializer, QuestionCreateSerializer, QuestionSerializer, TestCaseSerializer, TestCasesCreateSerializer
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
        if serializer.instance.author != user_profile:
            raise PermissionDenied("You can only update your own questions.")
        serializer.save()

    def perform_destroy(self, instance):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        if instance.author != user_profile:
            raise PermissionDenied("You can only delete your own questions.")
        instance.delete()

class CourseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsHolderOrParticipantPermission]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()

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
        if serializer.instance.author != user_profile:
            raise PermissionDenied("You can only update your own testcase.")
        serializer.save()

    def perform_destroy(self, instance):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        if instance.author != user_profile:
            raise PermissionDenied("You can only delete your own testcase.")
        instance.delete()

# class SubmissionViewSet(ModelViewSet):
#     queryset = Submission.objects.all()
#     serializer_class = SubmissionSerializer
#     permission_classes = [IsAuthenticated, SubmissionAccessPermission, SubmissionSituationEditPermission]

#     def perform_create(self, serializer):
#         user_profile = self.request.user.user

#         if user_profile.role != UserProfile.ROLE_PARTICIPANT:
#             raise PermissionDenied("Only participants can create submissions.")

#         serializer.save(participant=user_profile)
