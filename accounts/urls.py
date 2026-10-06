from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import api_views
from rest_framework.authtoken import views as token_view
urlpatterns = [
    path("register/",api_views.UserRegisterView.as_view()),
    path('profile/',api_views.UserProfileView.as_view()),
    path('changepassword/',api_views.ChangePasswordView.as_view()),
    path('admin/<int:pk>/',api_views.UserDetialView.as_view()),
    path('admin/<int:pk>/deactivate/',api_views.DeactivateView.as_view()),
    path('activate/<uid64>/<token>/',api_views.UserActivationAccountView.as_view()),
    path('forgot-password/',api_views.ForgotPasswordView.as_view()),
    path('reset-passwor/<uidb64>/<token>/',api_views.ResetPasswordView.as_view()),
    path('login/', api_views.UserLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



]
# 	"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4ODY5MTY3MSwiaWF0IjoxNzg4NjA1MjcxLCJqdGkiOiJlOTUyNjA1MGRkMjA0ZTk1ODE3YzNkZjViZmUxYWJkYSIsInVzZXJfaWQiOiIxIn0.Q3WJm74hDZRzGPyYIzXM08U4PZuPvqgnEKZ2Ml7MSXI",
	#"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4NjA1NTcxLCJpYXQiOjE3ODg2MDUyNzEsImp0aSI6ImFkMTc5OWU5NjUyMDQzNmI4ZDMzOTdlNTZlN2I3MDBiIiwidXNlcl9pZCI6IjEifQ.rrpgOMAd-t8Y_C_jmxs7lpWEVqEce26S599b-3jyxEI"