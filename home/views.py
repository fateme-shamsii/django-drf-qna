from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated


class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response({'masseages':'hello'})
