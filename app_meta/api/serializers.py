from rest_framework import serializers

class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer for basic information about an entity.
    """
    review_count = serializers.IntegerField(read_only=True, help_text="Total number of reviews on the platform.")
    average_count = serializers.DecimalField(read_only=True, max_digits=2, decimal_places=1, help_text="Average rating across all reviews.")
    business_profile_count = serializers.IntegerField(read_only=True, help_text="Total number of business profiles registered.")
    offer_count = serializers.IntegerField(read_only=True, help_text="Total number of offers available on the platform.")