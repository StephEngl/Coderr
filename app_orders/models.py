from django.db import models
from django.contrib.auth.models import User
from app_offers.models import OfferDetail


class Order(OfferDetail):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(User, related_name='orders_as_customer', on_delete=models.CASCADE)
    business_user = models.ForeignKey(User, related_name='orders_as_business', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
