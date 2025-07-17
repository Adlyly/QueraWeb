
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UserProfile
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'birth_date', 'phone', 'university', 'major', 'known_languages']
