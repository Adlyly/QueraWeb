from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from core.models import Question
from core.serializers import QuestionCreateSerializer, QuestionSerializer
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