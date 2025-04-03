from userprofile.models import UserProfile
from courses.models import Course
from django.db import models

class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL)
    courses = models.ManyToManyField(Course, related_name="questions")

class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="test_cases")
    input = models.TextField()
    output = models.TextField()