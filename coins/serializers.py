from coins.models import Coins, CoinPrices
from rest_framework import serializers


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.order_by('-time_open')[:5]
        return super(FilteredListSerializer, self).to_representation(data)


class PricePoint(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = CoinPrices
        fields = ('time_open', 'rate_open', 'coin_id')


class CoinsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=None)
    abbreviation = serializers.CharField(max_length=None)
    icon = serializers.CharField(max_length=None)
    coinprices_set = PricePoint(many=True, read_only=True)
