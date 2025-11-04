from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated  
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import ReviewSerializer, ReviewCreateUpdateSerializer
from ..models import Review

@extend_schema(tags=['Reviews'])
class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing review instances.
    """
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return ReviewCreateUpdateSerializer
        return ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)