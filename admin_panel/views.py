from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from users.models import CustomUser
from tasks.models import Task
from .forms import UserForm, TaskForm
from .permissions import superadmin_required, admin_or_superadmin_required

@login_required
def admin_logout(request):
    logout(request)
    return redirect('login')

@login_required
@admin_or_superadmin_required
@never_cache
def dashboard(request):
    if request.user.role == 'SuperAdmin':
        tasks = Task.objects.all()
        users = CustomUser.objects.all()
    else:
        users = CustomUser.objects.filter(managed_by=request.user)
        tasks = Task.objects.filter(assigned_to__managed_by=request.user)

    context = {
        'total_tasks': tasks.count(),
        'pending_tasks': tasks.filter(status='Pending').count(),
        'in_progress_tasks': tasks.filter(status='In Progress').count(),
        'completed_tasks': tasks.filter(status='Completed').count(),
        'recent_completed_tasks': tasks.filter(status='Completed').order_by('-updated_at')[:5],
        'total_users': users.count(),
        'admin_count': users.filter(role='Admin').count(),
        'user_count': users.filter(role='User').count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@superadmin_required
@never_cache
def user_list(request):
    users = CustomUser.objects.exclude(role='SuperAdmin').exclude(is_superuser=True)
    return render(request, 'admin_panel/user_list.html', {'users': users})

@login_required
@superadmin_required
@never_cache
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('admin_panel:user_list')
    else:
        form = UserForm()
    return render(request, 'admin_panel/user_form.html', {'form': form, 'action': 'Create'})

@login_required
@superadmin_required
@never_cache
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_panel:user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'admin_panel/user_form.html', {'form': form, 'action': 'Edit'})

@login_required
@superadmin_required
@never_cache
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('admin_panel:user_list')
    return render(request, 'admin_panel/user_confirm_delete.html', {'user': user})

@login_required
@admin_or_superadmin_required
@never_cache
def task_list(request):
    if request.user.role == 'SuperAdmin':
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to__managed_by=request.user)
    return render(request, 'admin_panel/task_list.html', {'tasks': tasks})

@login_required
@admin_or_superadmin_required
@never_cache
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully.')
            return redirect('admin_panel:task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'admin_panel/task_form.html', {'form': form, 'action': 'Create'})

@login_required
@admin_or_superadmin_required
@never_cache
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('admin_panel:task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'admin_panel/task_form.html', {'form': form, 'action': 'Edit'})

@login_required
@admin_or_superadmin_required
@never_cache
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('admin_panel:task_list')
    return render(request, 'admin_panel/task_confirm_delete.html', {'task': task})

@login_required
@admin_or_superadmin_required
@never_cache
def task_report(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.status != 'Completed':
        messages.error(request, 'Report is only available for completed tasks.')
        return redirect('admin_panel:task_list')
    return render(request, 'admin_panel/task_report.html', {'task': task})