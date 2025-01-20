from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    TYPE_CHOICES = [
        ('business', 'BUSINESS'),
        ('customer', 'CUSTOMER')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    working_hours = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='customer')
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
