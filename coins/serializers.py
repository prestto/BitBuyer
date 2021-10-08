from rest_framework import serializers


class CoinSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)