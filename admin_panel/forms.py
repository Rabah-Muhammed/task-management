from django import forms
from tasks.models import Task
from users.models import CustomUser

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': ''}),
            'description': forms.Textarea(attrs={'placeholder': ''}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': ''}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'Admin':
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(managed_by=user, role='User')
        elif user and user.role == 'SuperAdmin':
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(role='User')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ''}), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ''}), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'managed_by', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': ''}),
            'email': forms.EmailInput(attrs={'placeholder': ''}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data