from django.db.models import Min

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import OffersSerializer, OfferDetailDetailsSerializer, OfferCreateUpdateSerializer, OfferDetailSerializer
from app_offers.models import Offer, OfferDetail
from .permissions import IsBusinessUser, IsOwnerOfOffer
from .filters import OfferFilter
from .pagination import StandardResultsSetPagination


@extend_schema(
    tags=['Offers'],
    description="API endpoint for managing offers.",
)
class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing offers.

    Actions:
        list: List all offers.
        create: Create a new offer.
        retrieve: Retrieve a specific offer by ID.
        partial_update: Partially update an existing offer.
        destroy: Delete an existing offer.
    """
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        )

    def get_permissions(self):
        """
        Assign permissions based on action.
        Checks: authentication -> object existence -> ownership.
        """
        # Always require authentication first
        permission_classes = [IsAuthenticated]
        if self.action == 'list':
            permission_classes = [AllowAny]
        if self.action == 'create':
            permission_classes.append(IsBusinessUser)
        if self.action in ['partial_update', 'destroy']:
            permission_classes.append(IsOwnerOfOffer)
        return [perm() for perm in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OfferDetailSerializer
        if self.action in ['create', 'partial_update']:
            return OfferCreateUpdateSerializer
        return OffersSerializer

    @extend_schema(
        responses={
            200: OffersSerializer,
            400: OpenApiResponse(description="Bad Request"),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={
            201: OfferCreateUpdateSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="User is unauthorized"),
            403: OpenApiResponse(description="User is no business user"),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Saves an offer with the current user as creator.
        """
        serializer.save(user=self.request.user)

    @extend_schema(
        responses={
            200: OfferDetailSerializer,
            401: OpenApiResponse(description="User is unauthorized"),
            404: OpenApiResponse(description="Offer not Found"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OfferCreateUpdateSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="User is unauthorized"),
            403: OpenApiResponse(description="User is not the offer owner"),
            404: OpenApiResponse(description="Offer not Found"),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = OfferCreateUpdateSerializer(
            instance, context=self.get_serializer_context())
        return Response(serializer.data)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Offer deleted successfully"),
            401: OpenApiResponse(description="User is unauthorized"),
            403: OpenApiResponse(description="User is not the offer owner"),
            404: OpenApiResponse(description="Offer not Found"),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    tags=['Offers'],
    description="API view to retrieve details of a specific offer.",
    responses={
        200: OfferDetailDetailsSerializer,
        401: OpenApiResponse(description="User is unauthorized"),
        404: OpenApiResponse(description="Offer detail not found"),
    }
)
class OfferDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific offer.

    Methods:
        get: Retrieve offer details by ID.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailDetailsSerializer
    permission_classes = [IsAuthenticated]
