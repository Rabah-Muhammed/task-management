from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegisterSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role in ['Admin', 'SuperAdmin']:
                login(request, user)
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request, "Only Admin and SuperAdmin can login.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'admin_panel/login.html')