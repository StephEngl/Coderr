from rest_framework import serializers

from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing review details.
    """
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating reviews.
    """
    class Meta:
        model = Review
        fields = ['business_user', 'rating', 'description']