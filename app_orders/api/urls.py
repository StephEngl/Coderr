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