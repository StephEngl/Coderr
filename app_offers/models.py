from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='offer_images/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_delivery_time = models.IntegerField(help_text="Delivery time in days", null=True, blank=True)

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, related_name="details", on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

    def __str__(self):
        return f"Detail {self.id} for Offer {self.offer_id}"
