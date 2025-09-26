from django.contrib.auth.models import User
from rest_framework import serializers

from app_offers.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for offer details.
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class OffersSerializer(serializers.ModelSerializer):
    """
    Serializer for user offers with nested details and user info.
    """
    details = OfferDetailSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time', 'user_details'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def get_user_details(self, obj: Offer):
        user = obj.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }   