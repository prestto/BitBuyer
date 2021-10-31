from coins.models import Coins, CoinPrices, CurrentPrices
from rest_framework import serializers


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = reversed(data.order_by('-time_period_end')[:5])
        return super(FilteredListSerializer, self).to_representation(data)


class PricePoint(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = CoinPrices
        fields = ('time_close', 'rate_close', 'coin_id')


class CurrentPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentPrices
        fields = ('coin_id', 'rate_open', 'rate_close', 'time_period_end')


class CoinListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=None)
    abbreviation = serializers.CharField(max_length=None)
    icon = serializers.CharField(max_length=None)
    coinprices_set = PricePoint(many=True, read_only=True)
    currentprices = CurrentPriceSerializer(read_only=True)


class FilteredDetailSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = reversed(data.order_by('-time_period_end')[:30])
        return super(FilteredDetailSerializer, self).to_representation(data)


class ThirtyDayPricePoint(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredDetailSerializer
        model = CoinPrices
        fields = ('time_close', 'rate_close', 'coin_id')


class CoinDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=None)
    abbreviation = serializers.CharField(max_length=None)
    # icon = serializers.CharField(max_length=None)
    description = serializers.CharField(max_length=None)
    coinprices_set = ThirtyDayPricePoint(many=True, read_only=True)
