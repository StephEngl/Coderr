"""
URL configuration for review-related endpoints.

Defines RESTful routes for:
- Managing reviews through a viewset.

Conventions:
- Uses a router for automatic route generation.
- Each route includes a name for reverse URL resolution.

Example usage (reverse):
    reverse('reviews-list')
    reverse('reviews-detail', args=[1])
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet


router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]