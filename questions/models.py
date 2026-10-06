from django.db import models
from core.models import BaseModel
from django.conf import settings
# Create your models here.

class QuestionModel (BaseModel):
    auther = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='Questions')
    title = models.CharField(max_length=255,db_index=True)
    body = models.TextField()
    views_count = models.PositiveIntegerField(default=0)
    answers_count = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)
    accepted_answer = models.OneToOneField('answers.AnswersModel', null = True , blank=True, on_delete=models.SET_NULL,related_name='accepted_for_questions')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

