from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..models import Order
from .serializers import OrderSerializer, OrderCreateUpdateSerializer, OrderUpdateSerializer
from .permissions import IsAdminUser, IsCustomerUser
from app_offers.api.permissions import IsBusinessUser
from app_offers.models import OfferDetail
from app_auth.models import UserProfile


@extend_schema(
    tags=['Orders'],
    description="API endpoint for managing orders.",
)
class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing order instances.

    Actions:
        list: List all orders.
        create: Create a new order.
        partial_update: Partially update an existing order.
        destroy: Delete an existing order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        """
        Assign permissions based on action.
        Checks: authentication -> object existence -> ownership.
        """
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes.append(IsCustomerUser)
        if self.action == 'partial_update':
            permission_classes.append(IsBusinessUser)
        if self.action == 'destroy':
            permission_classes.append(IsAdminUser)
        return [perm() for perm in permission_classes]


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderSerializer
        if self.action == 'create':
            return OrderCreateUpdateSerializer
        if self.action == 'partial_update':
            return OrderUpdateSerializer
        return OrderSerializer

    @extend_schema(
        responses={
            201: OrderCreateUpdateSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="User is unauthorized"),
            403: OpenApiResponse(description="User is no customer user"),
            404: OpenApiResponse(description="Order not found"),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        offer_detail_id = self.request.data.get('offer_detail_id')
        offer_detail = get_object_or_404(OfferDetail, pk=offer_detail_id)
        serializer.save(customer_user=self.request.user, offer_detail=offer_detail)

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        """
        Disable GET /api/orders/{id}/
        """
        raise MethodNotAllowed('GET')
    

    @extend_schema(
        responses={
            200: OrderCreateUpdateSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="User is unauthorized"),
            403: OpenApiResponse(description="User is not the offer owner"),
            404: OpenApiResponse(description="Offer not Found"),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class OrderCountView(generics.ListAPIView):
    """
    API endpoint to get the count of orders in progress for the wanted user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    @extend_schema(
        tags=['Orders'],
        description="Get the count of orders for the wanted user.",
        responses={
            200: OpenApiResponse(description="Returns the count of orders."),
            401: OpenApiResponse(description="User is unauthorized"),
            404: OpenApiResponse(description="Found no business-user with this ID"),
        }
    )
    def get(self, request, business_user_id, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user_id=business_user_id, type='business')
        business_user = user_profile.user
        order_count = Order.objects.filter(business_user=business_user, status='in_progress').count()
        return Response({'order_count': order_count})


class CompletedOrderCountView(generics.ListAPIView):
    """
    API endpoint to get the count of completed orders for the wanted user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    @extend_schema(
        tags=['Orders'],
        description="Get the count of completed orders for the wanted user.",
        responses={
            200: OpenApiResponse(description="Returns the count of completed orders."),
            401: OpenApiResponse(description="User is unauthorized"),
            404: OpenApiResponse(description="Found no business-user with this ID"),
        }
    )
    def get(self, request, business_user_id, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user_id=business_user_id, type='business')
        business_user = user_profile.user
        completed_order_count = Order.objects.filter(business_user=business_user, status='completed').count()
        return Response({'completed_order_count': completed_order_count})