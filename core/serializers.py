from core.models import Course, Question, Submission, TestCase
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from userprofile.models import UserProfile

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username']

class QuestionSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'author']

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'description']
        read_only_fields = ['author']

class CourseSerializer(serializers.ModelSerializer):
    participants = UserProfileSerializer(many=True, read_only=True)
    holders = UserProfileSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=UserProfile.objects.all(), required=False
    )
    holders = serializers.PrimaryKeyRelatedField(
        many=True, queryset=UserProfile.objects.all()
    )
    questions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all(), required=False
    )

    class Meta:
        model = Course
        fields = ['title', 'start_date', 'end_date', 'description', 'participants', 'holders', 'questions']

class TestCaseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()

    class Meta:
        model = TestCase
        fields = ['id', 'input', 'output', 'author', 'question']

    def get_author(self, obj):
        return obj.author.user.username if obj.author and obj.author.user else None

    def get_question(self, obj):
        return obj.question.title if obj.question else None

class TestCasesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input', 'output', 'question']
        read_only_fields = ['author']

# class SubmissionSerializer(serializers.ModelSerializer):
#     participant = serializers.ReadOnlyField(source='participant.user.username')
#     course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
#     question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

#     class Meta:
#         model = Submission
#         fields = ['id', 'situation', 'participant', 'course', 'question']
#         read_only_fields = ['participant']

#     def get_queryset(self):
#         user = self.request.user
#         user_profile = user.user

#         if user.is_superuser:
#             return Submission.objects.all()

#         if user_profile.role == UserProfile.ROLE_PARTICIPANT:
#             return Submission.objects.filter(participant=user_profile)

#         if user_profile.role == UserProfile.ROLE_HOLDER:
#             return Submission.objects.filter(course__holders=user_profile)
#         return Submission.objects.none()


#     def validate(self, attrs):
#         request = self.context['request']
#         user_profile = request.user.user

#         if user_profile.role == UserProfile.ROLE_PARTICIPANT and 'situation' in attrs:
#             raise serializers.ValidationError({"situation": "Only course holders can set or modify situation."})

#         return attrs

#     def update(self, instance, validated_data):
#         request = self.context['request']
#         user_profile = request.user.user

#         if 'situation' in validated_data:
#             if not instance.course.holders.filter(id=user_profile.id).exists():
#                 raise serializers.ValidationError({"situation": "Only course holders can update situation."})

#         return super().update(instance, validated_data)
