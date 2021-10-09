from django.db import models

class Coins(models.Model):
    """
    Stores an instance of a coin, with metadata about the coin
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=31)
    abbreviation = models.CharField(max_length=7, unique=True)
    description = models.CharField(max_length=3000)
    icon = models.CharField(max_length=27)

    class Meta:
        db_table = 'coins'

class CoinPrices(models.Model):
    """
    Stores daily prices for coins
    """
    id = models.AutoField(primary_key=True)
    coin = models.ForeignKey(Coins, on_delete=models.CASCADE)
    rate_close = models.DecimalField(max_digits=5, decimal_places=2)
    rate_high = models.DecimalField(max_digits=5, decimal_places=2)
    rate_low = models.DecimalField(max_digits=5, decimal_places=2)
    rate_open = models.DecimalField(max_digits=5, decimal_places=2)
    time_close = models.DateTimeField()
    time_open = models.DateTimeField()
    time_period_end = models.DateTimeField()
    time_period_start = models.DateTimeField()
    class Meta:
        db_table = 'coin_prices'
