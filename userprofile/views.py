from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from core.models import User
from .serializers import UserTokenSerializer, UserSerializer, RegisterSerializer
from .models import UserToken, UserProfile
from .utils import create_token, validate_token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsAuthenticatedUser 

@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    remember_me = request.data.get("remember_me", False)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "Invalid username"}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, expiry = create_token(user, remember_me)
    userprofile = UserProfile.objects.filter(user=user)
    token_instance = UserTokenSerializer(data={
        "user": userprofile,
        "token": token,
        "expiry": expiry
    })
    if token_instance.is_valid():
        token_instance.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(token_instance.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout_view(request):
    token = request.headers.get("Authorization")

    if not token:
        return Response({"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

    if token.startswith("Bearer "):
        token = token[7:]

    deleted, _ = UserToken.objects.filter(token=token).delete()
    if deleted:
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdmin]) 
def admin_dashboard(request):
    token = request.headers.get("Authorization")
    user = validate_token(token)

    if not user:
        return Response({"error": "Unauthorized"}, status=401)
    
    if not user.is_staff:
        return Response({"error": "Forbidden"}, status=403)

    return Response({"message": f"Hello Admin {user.username}!"})

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAuthenticatedUser]) 
def user_dashboard(request):
    token = request.headers.get("Authorization")
    user = validate_token(token)

    if not user:
        return Response({"error": "Unauthorized"}, status=401)

    return Response({"message": f"Hello User {user.username}!"})

@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data=request.data) 
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)