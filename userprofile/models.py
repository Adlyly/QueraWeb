from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return f"{self.name} ({self.level})"


class UserProfile(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50)
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=50)
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='user')
    known_languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
