from rest_framework.views import APIView
from rest_framework.response import Response
from questions.selectors import get_by_id
from .selectors import get_answer_for_question, get_answer_by_id
from .serializer import ShowAnswerSerialaizer,CreateAnswerSerialaizer
from .services import  AnswerService
from rest_framework.permissions import IsAuthenticated
from core.permision import IsOwnerOrReadOnly
from rest_framework import status
class ShowAnswers(APIView):
    def get(self,request,qid):
        question = get_by_id(qid=qid)
        answers = get_answer_for_question( qs= question)
        serializer = ShowAnswerSerialaizer(instance = answers, many = True)
        return Response(serializer.data)

class CreateAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,question_id):
        question = get_by_id(qid = question_id)
        serializer = CreateAnswerSerialaizer(data = request.data)
        serializer.is_valid(raise_exception=True)
        answer = AnswerService.creat_answer(question=question,auther= request.user ,body=serializer.validated_data['body'])
        return Response(ShowAnswerSerialaizer(instance = answer).data)

    
class DeleteAnswerView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def delete(self,request,answer_id):
        answer = get_answer_by_id(answer_id=answer_id)
        self.check_object_permissions(request, answer)
        AnswerService.delete(answer=answer)
        return Response(
            {"message": "Answer deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )