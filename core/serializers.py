from core.models import Course, Question
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'author']

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'description']
        read_only_fields = ['author']

class CourseSerializer(serializers.ModelSerializer):
    holders = UserSerializer(read_only=True, many=True)
    participants = UserSerializer(read_only=True, many=True)
    questions = QuestionSerializer(read_only=True, many=True)
    class Meta:
        model = Course
        fields = ['title', 'created_at', 'start_date', 'end_date', 'holders', 'participants', 'questions']
