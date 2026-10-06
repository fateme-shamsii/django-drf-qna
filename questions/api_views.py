from rest_framework.views import APIView
from rest_framework.response import Response
from .models import QuestionModel
from .serializer import AllquestionsToSerializer, QuestionDetailSerializer,createSerializer,UpdateSerializer
from rest_framework.permissions import IsAuthenticated
from .services import QuestionServices
from rest_framework import status
from core.permision import IsOwnerOrReadOnly
from .selectors import get_by_id
from  answers.selectors import get_answer_by_id

class AllQuestionsView(APIView):
    def get(self,request):
        questions = QuestionModel.objects.all()
        q_serializer = AllquestionsToSerializer(instance= questions , many = True)
        return Response(q_serializer.data)

class QuestionDetialView(APIView):
    def get(self,request,id):
        question = QuestionModel.objects.get(id = id)
        q_serializer = QuestionDetailSerializer(instance = question)
        QuestionServices.increment_views(question =  question)
        return Response(q_serializer.data)

class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        serializer = createSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = QuestionServices.create_class(
            auther=request.user,
            title=serializer.validated_data['title'],
            body=serializer.validated_data['body']
        )

        return Response(
            QuestionDetailSerializer(instance=question).data
        )

class DeleteQuestionView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def delete(self,request,qid):
        question = get_by_id(qid = qid)
        self.check_object_permissions(request,question)
        QuestionServices.delete_question(question) 
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateQuestionView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def patch(self, request,qid):
        question = get_by_id(qid = qid)
        self.check_object_permissions(request,question)
        serializer = UpdateSerializer(
            instance=question,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(QuestionDetailSerializer(instance = question).data)

class AnswerAccceptView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def post(self,request,question_id,answer_id):
        qeustion = get_by_id(qid = question_id)
        self.check_object_permissions(request,qeustion)  
        answer = get_answer_by_id(answer_id = answer_id)
        QuestionServices.accept_answer(question = qeustion, answer= answer, accepted_by=request.user)
        return Response({'massegae':"answer accepted"})






