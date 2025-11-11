from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    file = models.FileField(upload_to='profile_pics/', null=True, blank=True)
    file_uploaded_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True, default='')
    tel = models.CharField(max_length=20, null=True, blank=True, default='')
    description = models.TextField(null=True, blank=True, default='')
    working_hours = models.CharField(max_length=100, null=True, blank=True, default='')
    type = models.CharField(choices=USER_TYPE_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_file = UserProfile.objects.get(pk=self.pk).file
            if old_file != self.file:
                self.file_uploaded_at = timezone.now().strftime('%Y-%m-%dT%H:%M:%S')
        super().save(*args, **kwargs)
