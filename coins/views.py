from coins.models import Coins
from coins.paginators import StandardResultsSetPagination
from coins.serializers import CoinListSerializer, CoinDetailSerializer
from rest_framework import viewsets
from rest_framework import mixins


class CoinViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = Coins.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    serializer_class = CoinListSerializer
    ordering = ['id']
    lookup_field = 'abbreviation'

    def get_serializer_class(self):
        if self.action == 'list':
            return CoinListSerializer
        if self.action == 'retrieve':
            return CoinDetailSerializer
