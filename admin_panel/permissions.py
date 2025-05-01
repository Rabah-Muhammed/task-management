from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def is_superadmin(user):
    return user.is_authenticated and user.role == 'SuperAdmin'

def is_admin_or_superadmin(user):
    return user.is_authenticated and user.role in ['Admin', 'SuperAdmin']

superadmin_required = user_passes_test(is_superadmin, login_url='/admin-panel/login/')
admin_or_superadmin_required = user_passes_test(is_admin_or_superadmin, login_url='/admin-panel/login/')