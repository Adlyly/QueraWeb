from django.contrib.auth.models import AbstractUser
from userprofile.models import UserProfile
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

class Question(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True)
    participants = models.ManyToManyField(UserProfile, related_name="participant_courses", limit_choices_to={'role': 'participant'}, blank=True )
    holders = models.ManyToManyField(UserProfile, related_name="holder_courses", limit_choices_to={'role': 'holder'})
    questions = models.ManyToManyField(Question, related_name="courses", blank=True)

    def __str__(self):
        return self.title

class TestCase(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
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
    situation = models.CharField(max_length=10, choices=SITUATION_CHOICES, null=True)
    participant = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name="submissions",
        limit_choices_to={'role': 'participant'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="submissions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="submissions")