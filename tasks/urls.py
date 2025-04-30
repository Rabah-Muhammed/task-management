from django.urls import path
from .views import TaskListView, TaskUpdateView, TaskReportView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/report/', TaskReportView.as_view(), name='task-report'),
]