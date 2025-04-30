from rest_framework import serializers
from .models import Task
from users.models import CustomUser

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        read_only_fields = ['completion_report', 'worked_hours']  

class TaskUpdateSerializer(serializers.ModelSerializer):
    completion_report = serializers.CharField(required=False, allow_blank=True)
    worked_hours = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        """Ensure completion_report and worked_hours are provided when status is Completed."""
        if data.get('status') == 'Completed':
            if not data.get('completion_report'):
                raise serializers.ValidationError({"completion_report": "This field is required when marking a task as Completed."})
            if data.get('worked_hours') is None or data.get('worked_hours') <= 0:
                raise serializers.ValidationError({"worked_hours": "A positive number of worked hours is required when marking a task as Completed."})
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completion_report', 'worked_hours']