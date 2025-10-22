from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Order
from .serializers import OrderSerializer, OrderCreateUpdateSerializer
from .permissions import IsAdminUser, IsCustomerUser
from app_offers.api.permissions import IsBusinessUser

class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing order instances.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    # def get_permissions(self):
    #     """
    #     Assign permissions based on action.
    #     Checks: authentication -> object existence -> ownership.
    #     """
    #     permission_classes = [IsAuthenticated]
    #     if self.action == 'create':
    #         permission_classes.append(IsCustomerUser)
    #     if self.action == 'partial_update':
    #         permission_classes.append(IsBusinessUser)
    #     if self.action == 'destroy':
    #         permission_classes.append(IsAdminUser)
    #     return [perm() for perm in permission_classes]


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderSerializer
        if self.action in ['create', 'partial_update']:
            return OrderCreateUpdateSerializer
        return OrderSerializer


    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)