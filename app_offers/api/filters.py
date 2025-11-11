from django_filters import rest_framework as filters
from app_offers.models import Offer

class OfferFilter(filters.FilterSet):
    """
    FilterSet for filtering offers based on minimum price and delivery time.
    """
    creator_id = filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_delivery_time = filters.NumberFilter(field_name='min_delivery_time', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']