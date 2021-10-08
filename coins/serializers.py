from rest_framework import serializers


class CoinSerializer(serializers.Serializer):
    class Meta:
        fields = ['name',]