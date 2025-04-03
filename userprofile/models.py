from django.conf import settings
from django.db import models

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
#     LANGUAGE_C = 'C'
#     LANGUAGE_CPP = 'CPP'
#     LANGUAGE_PYTHON = 'python'
#     LANGUAGE_Java = 'java'
#     LANGUAGE_CSharp = 'C#'
#     LANGUAGE_DJANGO = 'django'

#     LANGUAGE_CHOICES = [
#         (LANGUAGE_C, 'C'),
#         (LANGUAGE_CPP, 'CPP'),
#         (LANGUAGE_PYTHON, 'python'),
#         (LANGUAGE_Java, 'java'),
#         (LANGUAGE_CSharp, 'C#'),
#         (LANGUAGE_DJANGO, 'django'),
#     ]
#     langu = models.CharField(
#         max_length=1, choices=LANGUAGE_CHOICES, default=LANGUAGE_C)

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