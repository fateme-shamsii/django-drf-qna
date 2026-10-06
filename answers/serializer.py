from rest_framework import serializers
from .models import AnswersModel


class ShowAnswerSerialaizer(serializers.ModelSerializer):
    auther_email = serializers.CharField(source = "auther.email",read_only = True)
    class Meta:
        model = AnswersModel
        fields = ['id','question', 'body','score','is_accepted','created','auther_email']

class CreateAnswerSerialaizer(serializers.Serializer) :
    body = serializers.CharField()      