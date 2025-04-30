from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer
from .permissions import IsAdminOrSuperAdmin

class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return tasks assigned to the logged-in user."""
        return Task.objects.filter(assigned_to=self.request.user)

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Ensure the user can only update their own tasks."""
        obj = super().get_object()
        if obj.assigned_to != self.request.user:
            raise PermissionDenied("You can only update your own tasks.")
        return obj

class TaskReportView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskReportSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_object(self):
        """Ensure the task is Completed before accessing the report."""
        obj = super().get_object()
        if obj.status != 'Completed':
            raise ValidationError("Report is only available for completed tasks.")
        return obj