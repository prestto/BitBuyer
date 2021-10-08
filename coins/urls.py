from django.urls import path

from coins.views import ListCoins

urlpatterns = [
    path('', ListCoins.as_view(), name='coins-list'),
]
