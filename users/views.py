from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]