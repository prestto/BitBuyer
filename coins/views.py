from rest_framework.response import Response
from rest_framework.views import APIView

from coins.serializers import CoinSerializer
from rest_framework import status

class ListCoins(APIView):
    def get(self, request, format=None):
        return Response(CoinSerializer({'name': 'BTC'}).data, status=status.HTTP_200_OK)
