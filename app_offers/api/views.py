from django.db.models import Q, Min
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions, generics, request, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

from app_offers import models
from app_offers.api.serializers import OffersSerializer, OfferDetailDetailsSerializer, OfferCreateUpdateSerializer, OfferDetailWriteSerializer, OfferDetailURLSerializer, OfferDetailSerializer
from app_offers.models import Offer, OfferDetail
from .permissions import IsBusinessUser, IsOwnerOfOffer
from .filters import OfferFilter

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
    queryset = Offer.objects.annotate(
        min_price=Min('details__price'),
        min_delivery_time=Min('details__delivery_time_in_days')
    )
    permission_classes = [AllowAny]
    # http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OfferFilter
    # filterset_fields = ['user__id']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['min_price']
    pagination_class = PageNumberPagination

    def get_permissions(self):
        """
        Assign permissions based on action.
        """
        permissions_list = super().get_permissions()
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        if self.action == 'create':
            permissions_list.append(IsBusinessUser())
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions_list.append(IsOwnerOfOffer())
        return permissions_list
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OfferDetailSerializer
        if self.action in ['create', 'partial_update']:
            return OfferCreateUpdateSerializer
        return OffersSerializer
    
    def perform_create(self, serializer):
        """
        Saves a task with the current user as creator.
        """
        serializer.save(user=self.request.user)


class OfferDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific offer.

    Methods:
        get: Retrieve offer details by ID.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailDetailsSerializer
    permission_classes = [IsAuthenticated]