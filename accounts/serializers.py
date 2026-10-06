from rest_framework import serializers
from .models import User
from  questions.models import QuestionModel
from questions.serializer import AllquestionsToSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "is_active", "is_staff", "date_joined", "questions"]

    def get_questions(self, obj):
        qs = obj.Questions.all()
        return AllquestionsToSerializer(instance=qs, many=True).data

        
def clean_email(value):
    if "admin" in value:
        raise serializers.ValidationError('email cant contain admin ')

def validate_unique_email(value):
    check_email = User.objects.filter(email = value).exists()
    if check_email  == True :
        raise serializers.ValidationError('email is not unique')      

class UserRegisterSerializer(serializers.Serializer):

    email = serializers.EmailField(required = True,validators = [clean_email,validate_unique_email])
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True , write_only = True)
    password2 = serializers.CharField(required = True , write_only = True)


    def validate_username(self,value):
        if value == 'admin':
            raise serializers.ValidationError("you cant use admin in your username")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2'] :
            raise serializers.ValidationError('your password is not mach')
        return attrs



class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required = True , write_only = True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email

        return token