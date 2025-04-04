from django.conf import settings
from django.db import models
from datetime import datetime, timezone

class Language(models.Model):
    LEVEL_JUNIOR = 'junior'
    LEVEL_MIDLEVEL = 'mid_level'
    LEVEL_SENIOR = 'senior'
    LEVEL_CHOICES = [
        (LEVEL_JUNIOR, 'junior'),
        (LEVEL_MIDLEVEL, 'mid_level'),
        (LEVEL_SENIOR, 'senior'),
    ]
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default=LEVEL_JUNIOR)
    name = models.CharField(max_length=50, unique=True)


class UserProfile(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50)
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=50)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    known_languages = models.ManyToManyField(Language, blank=True)

class Participant(UserProfile):
    pass

class Holder(UserProfile):
    pass

class Admin(UserProfile):
    pass

class UserToken(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='token')
    token = models.CharField(max_length=100, unique=True)
    expiry = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expiry

    def refresh(self, remember_me=False):
        self.expiry = timezone.now() + datetime.timedelta(days=7 if remember_me else 1)
        self.save()