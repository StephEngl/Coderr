from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status, filters
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..models import Review
from .serializers import ReviewSerializer, ReviewCreateUpdateSerializer
from .permissions import IsReviewer
from .filters import ReviewFilter
from app_orders.api.permissions import IsCustomerUser


@extend_schema(
    tags=['Reviews'],
    description="API endpoint for managing orders.",
)
class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing, creating, updating, and deleting review instances.
    Provides filtering, ordering, and permission checks for review-related actions.
    """
    queryset = Review.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return ReviewCreateUpdateSerializer
        return ReviewSerializer

    def get_permissions(self):
        """
        Assign permissions based on action.
        Checks: authentication -> object existence -> ownership.
        """
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes.append(IsCustomerUser)
        if self.action == 'partial_update':
            permission_classes.append(IsReviewer)
        if self.action == 'destroy':
            permission_classes.append(IsReviewer)
        return [perm() for perm in permission_classes]

    @extend_schema(
        responses={
            200: ReviewSerializer(many=True),
            401: OpenApiResponse(description="User is unauthorized"),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        """
        Disable GET /api/orders/{id}/
        """
        raise MethodNotAllowed('GET')

    @extend_schema(
        responses={
            201: ReviewSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="User is unauthorized"),
            403: OpenApiResponse(description="User is no customer user"),
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new review instance.
        Returns the created review data or validation errors.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        read_serializer = ReviewSerializer(
            serializer.instance, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Create a new Review instance after validation.

        This method ensures that a user (reviewer) can only create one
        review per business user. If a review from the same reviewer
        to the same business user already exists, a ValidationError is raised.
        """
        business_user = serializer.validated_data['business_user']
        reviewer = self.request.user
        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise ValidationError({"business_user": "You have already reviewed this business user."})

        serializer.save(reviewer=self.request.user)

    @extend_schema(
        responses={
            200: ReviewSerializer,
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="User is unauthorized"),
            403: OpenApiResponse(description="User is not the offer owner"),
            404: OpenApiResponse(description="Review not Found"),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an existing Review instance.

        This method prevents changing the 'business_user' field of a review.
        Only other editable fields (e.g., rating or comment) can be modified.
        If an attempt is made to update the 'business_user' field, a ValidationError is raised.

        Returns the updated review data or validation errors.
        """
        business_user = request.data.get('business_user')
        if business_user:
            raise ValidationError({"detail": "Cannot change business_user of a review."})

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = ReviewSerializer(instance, context={'request': request})
        return Response(read_serializer.data)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Review deleted successfully"),
            401: OpenApiResponse(description="User is unauthorized"),
            403: OpenApiResponse(description="User is not review owner"),
            404: OpenApiResponse(description="Offer not Found"),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
