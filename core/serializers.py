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

class SubmissionSerializer(serializers.ModelSerializer):
    participant = serializers.ReadOnlyField(source='participant.user.username')
    situation = serializers.CharField(required=False)

    class Meta:
        model = Submission
        fields = '__all__'

    def validate(self, data):
        user_profile = UserProfile.objects.get(user=self.context['request'].user)

        if 'situation' in data:
            is_holder = False
            course_field = data.get('course') or getattr(self.instance, 'course', None)
            course_id = course_field.id if isinstance(course_field, Course) else course_field
            if course_id:
                try:
                    course = Course.objects.get(id=course_id)
                    is_holder = user_profile in course.holders.all()
                except Course.DoesNotExist:
                    pass
            if not is_holder:
                raise serializers.ValidationError({"situation": "Only the course holder can set the situation."})

        return data
