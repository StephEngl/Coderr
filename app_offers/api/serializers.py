from django.contrib.auth.models import User
from rest_framework import serializers

from app_offers.models import Offer, OfferDetail

# Für GET/Detail-Views (alle Felder inkl. id)
class OfferDetailDetailsSerializer(serializers.ModelSerializer):
    features = serializers.ListField(child=serializers.CharField(), allow_empty=True)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


# Für GET/Listen-Views (id, url)
class OfferDetailURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        extra_kwargs = {'url': {'view_name': 'offer-detail', 'lookup_field': 'pk'}}
        fields = ['id', 'url']


# Für POST/PUT (alle Felder, inkl. features als Array)
class OfferDetailWriteSerializer(OfferDetailDetailsSerializer):
    class Meta(OfferDetailDetailsSerializer.Meta):
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OffersSerializer(serializers.ModelSerializer):
    """
    Serializer for user offers with nested details and user info.
    """
    details = OfferDetailURLSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField(help_text="Delivery time in days")

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
    
    def get_min_price(self, obj: Offer):
        return getattr(obj, 'min_price', None)
    def get_min_delivery_time(self, obj: Offer):
        return getattr(obj, 'min_delivery_time', None)
    

class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating offers with nested details.
    """
    details = OfferDetailDetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        validated_data.pop('user', None)
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetail.objects.create(offer=instance, **detail_data)
        return instance
    

class OfferDetailSerializer(OffersSerializer):
    """
    Serializer for OfferDetail model.
    """
    class Meta(OffersSerializer.Meta):
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]
