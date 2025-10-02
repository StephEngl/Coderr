from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OfferViewSet, OfferDetailView

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offers')

urlpatterns = [
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('', include(router.urls)),
]
