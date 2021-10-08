from coins.models import Coins
from rest_framework import serializers


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins
        fields = ['id', 'name', 'abbreviation', 'description', 'icon']
