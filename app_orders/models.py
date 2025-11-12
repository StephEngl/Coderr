from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99999)])
    delivery_time_in_days = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(999)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    offer_type = models.CharField(max_length=30, default='basic')
    features = models.JSONField(default=list)

    customer_user = models.ForeignKey(User, related_name='orders_as_customer', on_delete=models.CASCADE)
    business_user = models.ForeignKey(User, related_name='orders_as_business', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
