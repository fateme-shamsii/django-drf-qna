from .models import QuestionModel
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import PermissionDenied, ValidationError

class QuestionServices:
    @staticmethod
    @transaction.atomic
    def create_class(*,auther,title,body):
        question = QuestionModel.objects.create(auther = auther , title = title, body = body)
        return question

    @staticmethod
    def increment_views(*,question):
        QuestionModel.objects.filter(id = question.id).update(
            views_count = F('views_count') + 1  
        )
    @staticmethod
    @transaction.atomic   
    def delete_question(question):
        question.delete() 
    @staticmethod
    @transaction.atomic
    def accept_answer(*, question, answer, accepted_by):
        if question.auther.id != accepted_by.id:
            raise PermissionDenied("Only question owner can accept answer")

        if answer.question.id != question.id:
            raise ValidationError("Answer does not belong to question")

        if question.accepted_answer:
            raise ValidationError("Question already has accepted answer")

        question.accepted_answer = answer
        question.save(update_fields=["accepted_answer"])
        answer.is_accepted = True
        answer.save(update_fields=["is_accepted"])
        return question



               

