"""
URL configuration for offer-related endpoints.

Defines RESTful routes for:
- Listing, creating, updating, and deleting offers.
- Retrieving detailed information for a specific offer.

Conventions:
- Uses a router for viewsets and a class-based view for detailed retrieval.
- Each route includes a name for reverse URL resolution.

Example usage (reverse):
    reverse('offers-list')
    reverse('offer-detail', args=[1])
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OfferViewSet, OfferDetailView


router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offers')

urlpatterns = [
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('', include(router.urls)),
]
