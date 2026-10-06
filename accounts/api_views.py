from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,UserSerializer,UserChangePasswordSerializer,ForgotPasswordSerializer,MyTokenObtainPairSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .selectors import get_user_all,get_user_by_email,get_user_by_id
from .services import update_profile,changepassword,deactive,create_user,buildreset_password_link,send_reset_password_email
from django.utils.http import urlsafe_base64_decode  
from django.contrib.auth.tokens import default_token_generator
from .models import User
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView



@extend_schema(request=UserRegisterSerializer,responses={200: UserSerializer})
class UserRegisterView(APIView):
    def post(self,request):
        serializer = UserRegisterSerializer(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user(email = serializer.validated_data['email'],username = serializer.validated_data['username'],password=serializer.validated_data['password'])

        return Response(UserSerializer(user).data  , status= status.HTTP_200_OK)        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serailizer = UserSerializer(request.user)
        return Response(serailizer.data)
    def put(self,request):
        uername = request.data.get("username")
        user = update_profile(user =request.user, username=uername)
        return Response(UserSerializer(request.user).data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        serializer = UserChangePasswordSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = changepassword(user = request.user , password= serializer.validated_data['new_password'])

        return Response({'massage' : "PAssword changed successfuly"})
    
class UserDetialView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,pk):
        user  = get_user_by_id(pk=pk)
        if not user:
            return Response({'massage' : "User  don't exit"})
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self,request,pk):  
        user  = get_user_by_id(pk=pk)
        if not user:
            return Response({'massage' : "User  don't exit"})
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeactivateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self,request,pk):
            user  = User.objects.get(id = pk)
            if not user:
                return Response({'massage' : "User  don't exit"})
            deactive(user=user)
            return Response({'massage' : "deactivate"})

class UserActivationAccountView(APIView):
    permission_classes = [AllowAny]
    def get(Self,request,uid64,token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk =uid)
        except Exception:
             return Response({'massage' : "invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user,token):

            user.is_active = True
            user.save(update_fields=['is_active'])
            return Response({'massage' : "Account Activated"})
        
        return Response({'massage' : "invalid link"}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
       serializer = ForgotPasswordSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       user = get_user_by_email(email = serializer.validated_data['email'])

       if user:
            reset_url = buildreset_password_link(user)
            send_reset_password_email(user= user, reset_url=reset_url)
       return Response({"message":"a reset link has been sen"})



class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,uidb64,token):
        serializer = UserChangePasswordSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_by_id(pk = uid)
        except Exception:
            return Response({'massage' : "invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user,token):
            return Response({'massage' : "invalid link"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message":"password reset successfully"})




     
class UserLoginView(TokenObtainPairView):
    serializer = MyTokenObtainPairSerializer
    
 