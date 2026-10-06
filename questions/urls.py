from django.contrib import admin
from django.urls import path,include
from . import api_views

urlpatterns = [
    path('',api_views.AllQuestionsView.as_view(), name='home'),
    path('<uuid:id>/',api_views.QuestionDetialView.as_view(),name= 'detail'),
    path("create/",api_views.QuestionCreateView.as_view()),
    path("delete/<uuid:qid>/",api_views.DeleteQuestionView.as_view()),
    path("update/<uuid:qid>/",api_views.UpdateQuestionView.as_view()),
    path("is_accept/<uuid:question_id>/<uuid:answer_id>/",api_views.AnswerAccceptView.as_view()),
]