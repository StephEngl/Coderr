from rest_framework import serializers
from rest_framework.exceptions import NotFound

from ..models import Order
from app_offers.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Order instances.

    Fields include users, order details, and status.
    'features' is a list of strings.
    """
    features = serializers.ListField(child=serializers.CharField(), allow_empty=True, read_only=True)
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
    """
    Serializer for creating and updating orders.

    'offer_detail_id' is required on input and write-only.
    'features' is a list of strings.
    Other fields are read-only, sourced from related OfferDetail.
    """
    features = serializers.ListField(child=serializers.CharField(), allow_empty=True, read_only=True)
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
        Create Order, preferring OfferDetail from caller.

        If `offer_detail` is None, resolve it from `offer_detail_id`.
        Raise 404 if OfferDetail not found.
        Returns created Order instance.
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
    """
    Serializer for partial update of Order instances.

    All fields except 'status' are read-only.
    'Status' can be updated to completed or cancelled.
    """
    class Meta(OrderCreateUpdateSerializer.Meta):
        read_only_fields = ['id', 'offer_detail_id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']