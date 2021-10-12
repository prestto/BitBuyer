from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from coins.models import Coins, CoinPrices
from coins.paginators import StandardResultsSetPagination
from coins.serializers import CoinsSerializer
from django.db import connection
from datetime import datetime, timedelta
import pytz
from rest_framework import serializers


class ListCoins(ListAPIView):
    
    queryset = Coins.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    serializer_class = CoinsSerializer
    ordering = ['id']
