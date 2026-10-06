from django.db import models
from core.models import BaseModel
from django.conf import settings
# Create your models here.

class AnswersModel (BaseModel):
    question = models.ForeignKey('questions.QuestionModel', on_delete=models.CASCADE,related_name='Answers')
    auther  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='Answers')
    body = models.TextField()
    is_accepted = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-is_accepted','-score','-created')

    def __str__(self):
        return f"anwers #{self.pk}"




