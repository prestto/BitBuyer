from coins.models import Coins
from rest_framework import mixins, viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin

from articles.serializers import ArticleListSerializer


class ArticleViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet,
                     NestedViewSetMixin):
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        return Coins.objects.prefetch_related('articleaggregates_set').filter(
            abbreviation=self.kwargs['parent_lookup_coins_abbreviation']
        ).values(
            'articleaggregates__coin_id', 'articleaggregates__end_time', 'articleaggregates__count'
        )
