from rest_framework import serializers

from articles.models import ArticleAggregates


class ArticleListSerializer(serializers.Serializer):
    coin_id = serializers.IntegerField(source='articleaggregates__coin_id')
    end_time = serializers.DateTimeField(source='articleaggregates__end_time')
    count = serializers.IntegerField(source='articleaggregates__count')
