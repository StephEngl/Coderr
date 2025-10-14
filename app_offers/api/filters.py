from django_filters import rest_framework as filters
from app_offers.models import Offer

class OfferFilter(filters.FilterSet):
    """
    FilterSet for filtering offers based on minimum price and delivery time.
    """
    creator_id = filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    min_price = filters.NumberFilter(method='filter_min_price')
    min_delivery_time = filters.NumberFilter(method='filter_min_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'min_delivery_time']
    
    def filter_min_price(self, queryset, name, value):
        # Filter auf den annotierten Wert min_price >= value
        return queryset.filter(min_price__gte=value)

    def filter_min_delivery_time(self, queryset, name, value):
        # Filter auf den annotierten Wert min_delivery_time >= value
        return queryset.filter(min_delivery_time__gte=value)