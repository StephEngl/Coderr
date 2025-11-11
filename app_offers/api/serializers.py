from rest_framework import serializers

from app_offers.models import Offer, OfferDetail

class OfferDetailDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail model with all fields for reading and writing.
    """
    features = serializers.ListField(child=serializers.CharField(), allow_empty=True)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailWriteSerializer(OfferDetailDetailsSerializer):
    """
    Serializer for writing OfferDetail objects (used for POST/PATCH).
    Excludes 'id' field.
    """
    class Meta(OfferDetailDetailsSerializer.Meta):
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailURLSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail model that returns only 'id' and 'url'.
    Used for nested representation in Offer list views.
    """
    class Meta:
        model = OfferDetail
        extra_kwargs = {'url': {'view_name': 'offer-detail', 'lookup_field': 'pk'}}
        fields = ['id', 'url']


class OffersSerializer(serializers.ModelSerializer):
    """
    Serializer for Offer model in list and retrieve views.
    Includes nested details as URLs, user info, and calculated fields.
    """
    details = OfferDetailURLSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False, read_only=True, help_text="Minimum price among all offer details." )
    min_delivery_time = serializers.IntegerField(read_only=True, help_text="Minimum delivery time in days among all offer details." )

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time', 'user_details'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'min_price', 'min_delivery_time', 'user_details']


    def get_user_details(self, obj: Offer):
        """
        Returns basic user info for the offer owner.
        """
        user = obj.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }


class OfferDetailSerializer(OffersSerializer):
    """
    Serializer for Offer model in retrieve view, excluding user_details.
    """
    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]


class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Offer objects with nested details.
    Used for POST and PATCH requests.
    """
    details = OfferDetailDetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']

    def validate_details(self, value):
        """
        Validates that at least three offer details are provided on POST.
        """
        if self.context['request'].method == 'POST':
            if len(value) < 3:
                raise serializers.ValidationError("At least three offer details are required.")
        return value

    def create(self, validated_data):
        """
        Creates an Offer and its related OfferDetail objects.
        """
        details_data = validated_data.pop('details', [])
        validated_data.pop('user', None)
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        """
        Updates Offer fields and nested OfferDetail objects by offer_type.
        Only the details provided in the request are updated.
        """
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if not offer_type:
                    continue
                try:
                    detail_instance = instance.details.get(offer_type=offer_type)
                except OfferDetail.DoesNotExist:
                    raise serializers.ValidationError(f"OfferDetail with offer_type '{offer_type}' does not exist.")
                for field, value in detail_data.items():
                    if field != 'offer_type':
                        setattr(detail_instance, field, value)
                detail_instance.save()
        return instance



