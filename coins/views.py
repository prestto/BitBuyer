from rest_framework.generics import ListAPIView

from coins.models import Coins
from coins.paginators import StandardResultsSetPagination
from coins.serializers import CoinsSerializer


class ListCoins(ListAPIView):

    queryset = Coins.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    serializer_class = CoinsSerializer
    ordering = ['id']
