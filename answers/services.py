from .models import AnswersModel
from questions.models import QuestionModel
from django.db import transaction
from django.db.models import F


class AnswerService:

    @staticmethod
    @transaction.atomic
    def creat_answer(*, auther, question, body):
        answer = AnswersModel.objects.create(auther = auther , question = question , body = body)
        QuestionModel.objects.filter(id = question.id).update(answers_count = F('answers_count') +1)
        return answer

    @staticmethod
    @transaction.atomic
    def delete(*,answer):
        question_id = answer.question.id
        answer.delete()
        QuestionModel.objects.filter(id = question_id).update(answers_count = F('answers_count') -1)


