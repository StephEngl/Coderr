from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

from app_offers.api.serializers import OffersSerializer, OfferDetailSerializer
from app_offers.models import Offer

class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing offers.

    Actions:
        list: List all offers.
        create: Create a new offer.
        retrieve: Retrieve a specific offer by ID.
        update: Update an existing offer.
        partial_update: Partially update an existing offer.
        destroy: Delete an existing offer.
    """
    queryset = Offer.objects.all()
    serializer_class = OffersSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination


class OfferDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific offer.

    Methods:
        get: Retrieve offer details by ID.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    # permission_classes = [IsAuthenticated]