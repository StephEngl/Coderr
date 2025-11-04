from rest_framework import serializers
from rest_framework.exceptions import NotFound

from ..models import Order
from app_offers.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'offer_detail_id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status']

    def create(self, validated_data, offer_detail=None, **kwargs):
        """
        Prefer the OfferDetail instance passed from the view via perform_create.
        Fallback: resolve from offer_detail_id and raise 404 if missing.
        """
        if offer_detail is None:
            offer_detail_id = validated_data.pop('offer_detail_id', None)
            if not offer_detail_id:
                raise serializers.ValidationError({"offer_detail_id": "This field is required."})
            try:
                offer_detail = OfferDetail.objects.get(pk=offer_detail_id)
            except OfferDetail.DoesNotExist:
                raise NotFound("OfferDetail not found.")
            
        user = self.context['request'].user
        
        order = Order.objects.create(
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            customer_user=user,
            business_user=offer_detail.offer.user,
            status='in_progress',
        )
        return order


class OrderUpdateSerializer(OrderCreateUpdateSerializer):
    class Meta(OrderCreateUpdateSerializer.Meta):
        read_only_fields = ['id', 'offer_detail_id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']