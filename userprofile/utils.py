import uuid
from datetime import timedelta
from django.utils.timezone import now
from .models import UserToken

def create_token(user, remember_me=False):
    token = str(uuid.uuid4())
    expiry = now() + (timedelta(days=7) if remember_me else timedelta(hours=1))
    UserToken.objects.create(user=user, token=token, expiry=expiry)
    return token, expiry

def validate_token(token, remember_me=False):
    try:
        user_token = UserToken.objects.get(token=token)
        if user_token.is_expired():
            if remember_me:
                user_token.refresh(remember_me=True)
            else:
                user_token.delete()
                return None
        return user_token.user
    except UserToken.DoesNotExist:
        return None
