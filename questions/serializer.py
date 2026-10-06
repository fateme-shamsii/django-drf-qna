from rest_framework import serializers
from .models import QuestionModel

class AllquestionsToSerializer(serializers.Serializer):
        
        id = serializers.UUIDField()
        title = serializers.CharField()
        body = serializers.CharField()
        views_count = serializers.CharField()

class QuestionDetailSerializer (serializers.ModelSerializer):
        auther_username = serializers.CharField(source = "auther.username")

        class Meta:
                model = QuestionModel
                exclude = ['auther']

class createSerializer(serializers.Serializer):
        title = serializers.CharField()
        body = serializers.CharField()

class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionModel
        fields = ["title", "body"]      
        