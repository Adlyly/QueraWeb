from userprofile.models import Participant,Holder,Admin
from questionsbank.models import Question
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True)
    participants = models.ManyToManyField(Participant, related_name="courses")
    holders = models.ManyToManyField(Holder, related_name="courses")
    admins = models.ManyToManyField(Admin, related_name="courses")

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