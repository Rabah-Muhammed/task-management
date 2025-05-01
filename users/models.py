from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('SuperAdmin', 'SuperAdmin'),
        ('Admin', 'Admin'),
        ('User', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')
    managed_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role__in': ['Admin', 'SuperAdmin']},
        related_name='managed_users'
    )

    
    def __str__(self):
        return self.username