from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from users import views as auth_views
from django.conf.urls.static import static
from admin_panel import views as admin_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin-panel/login/', auth_views.login_view, name='login'),
    path('admin-panel/logout/', admin_views.admin_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)