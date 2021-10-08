from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from coins.models import Coins
from coins.paginators import StandardResultsSetPagination
from coins.serializers import CoinSerializer


class ListCoins(ListAPIView):
    
    queryset = Coins.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = CoinSerializer