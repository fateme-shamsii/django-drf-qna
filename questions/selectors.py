from .models import QuestionModel


def get_by_id(*,qid):
    qs = QuestionModel.objects.get(id = qid)
    return qs