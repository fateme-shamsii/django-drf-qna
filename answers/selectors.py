from .models import AnswersModel

def get_answer_for_question(*,qs):
    return AnswersModel.objects.filter(question = qs)

def get_answer_by_id(*,answer_id):
    return AnswersModel.objects.filter(id = answer_id).first()

