from django.contrib.auth.models import AbstractUser
from userprofile.models import Admin, Holder, Participant, UserProfile
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

class Course(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True)
    participants = models.ManyToManyField(Participant, related_name="courses")
    holders = models.ManyToManyField(Holder, related_name="courses")
    admins = models.ManyToManyField(Admin, related_name="courses")

class Question(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField(Course, related_name="questions")

class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="test_cases")
    input = models.TextField()
    output = models.TextField()

class Submission(models.Model):
    SITUATION_CORRECT = 'correct'
    SITUATION_WRONG = 'wrong'
    SITUATION_CHOICES = [
        (SITUATION_CORRECT, 'correct'),
        (SITUATION_WRONG, 'wrong')
    ]
    situation = models.CharField(
        max_length=10, choices=SITUATION_CHOICES)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="submissions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="submissions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="submissions")