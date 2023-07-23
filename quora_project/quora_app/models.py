from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET(0))
    question_text=models.CharField(max_length=1000)

class Answer(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET(0), null=True)
    question=models.ForeignKey(Question, on_delete=models.SET(0))
    answer_text=models.TextField(max_length=50000)

class AnswerLike(models.Model):
    answer=models.ForeignKey(Answer, on_delete=models.SET(0))
    user=models.ForeignKey(User, on_delete=models.SET(0))