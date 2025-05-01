from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.contrib.auth import get_user_model

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to login and logout pages without token
        if request.path in ['/admin-panel/login/', '/admin-panel/logout/']:
            return self.get_response(request)

        # Check for JWT token in Authorization header
        if request.path.startswith('/admin-panel/'):
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                try:
                    jwt_auth = JWTAuthentication()
                    validated_token = jwt_auth.get_validated_token(token)
                    request.user = jwt_auth.get_user(validated_token)
                except (InvalidToken, AuthenticationFailed):
                    return HttpResponseRedirect(reverse('admin_panel:login'))
            else:
                return HttpResponseRedirect(reverse('admin_panel:login'))
        return self.get_response(request)