from userprofile.models import UserProfile
from django.db import models

class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField('courses.Course', related_name="questions")

class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="test_cases")
    input = models.TextField()
    output = models.TextField()