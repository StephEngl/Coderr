from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from core.utils import overwrite_file_upload


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to=overwrite_file_upload, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(Offer, related_name="details", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99999)])
    delivery_time_in_days = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(999)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    offer_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    features = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Detail {self.id} for Offer {self.offer_id}"

