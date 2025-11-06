"""
URL configuration for order-related endpoints.

Defines RESTful routes for:
- Managing orders through a viewset.
- Retrieving total and completed order counts per user.

Conventions:
- Uses a router for the main order viewset.
- Includes individual class-based views for order statistics.
- Each route is named for reverse URL resolution.

Example usage (reverse):
    reverse('orders-list')
    reverse('order-count', args=[1])
    reverse('completed-order-count', args=[1])
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, OrderCountView, CompletedOrderCountView


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
    path('', include(router.urls)),
]