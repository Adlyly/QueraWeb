from core.models import Course, Question
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
        fields = ['id', 'role', 'username']

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
        many=True, queryset=UserProfile.objects.filter(role='participant'), required=False
    )
    holders = serializers.PrimaryKeyRelatedField(
        many=True, queryset=UserProfile.objects.filter(role='holder')
    )
    questions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all(), required=False
    )

    class Meta:
        model = Course
        fields = '__all__'