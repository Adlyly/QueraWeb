
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UserToken, UserProfile
from core.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'birth_date', 'phone', 'university', 'major', 'known_languages']