from django.db.models import Avg

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from .serializers import BaseInfoSerializer
from app_reviews.models import Review
from app_auth.models import UserProfile
from app_offers.models import Offer

@extend_schema(
    tags=['Meta'],
    description="API endpoint for retrieving basic application information.",
    responses={200: BaseInfoSerializer},
)
class BaseInfoView(generics.RetrieveAPIView):
    """
    Retrieve basic information about the application.
    
    This view provides meta information such as the total number of reviews,
    average review rating, number of business profiles, and total offers.
    """
    serializer_class = BaseInfoSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to fetch application statistics.
        """
        average_rating = Review.objects.aggregate(average=Avg('rating'))['average'] or 0.0

        data = {
            "review_count": Review.objects.count(),
            "average_rating": average_rating,
            "business_profile_count": UserProfile.objects.filter(type='business').count(),
            "offer_count": Offer.objects.count(),
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)