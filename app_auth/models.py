from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='profile_pics/', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True, default='')
    tel = models.CharField(max_length=20, null=True, blank=True, default='')
    description = models.TextField(null=True, blank=True, default='')
    working_hours = models.CharField(max_length=100, null=True, blank=True, default='')
    
    def __str__(self):
        return f"{self.user.username} Profile"
