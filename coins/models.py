from django.db import models

class Coins(models.Model):
    """
    Stores an instance of a coin, with metadata about the coin
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=31)
    abbreviation = models.CharField(max_length=7, unique=True)
    description = models.CharField(max_length=10000)
    icon = models.CharField(max_length=27)

    class Meta:
        db_table = 'coins'

class CoinPrices(models.Model):
    """
    Stores daily prices for coins
    """
    id = models.AutoField(primary_key=True)
    coin = models.ForeignKey(Coins, on_delete=models.CASCADE)
    rate_close = models.DecimalField(max_digits=24, decimal_places=11)
    rate_high = models.DecimalField(max_digits=24, decimal_places=11)
    rate_low = models.DecimalField(max_digits=24, decimal_places=11)
    rate_open = models.DecimalField(max_digits=24, decimal_places=11)
    time_close = models.DateTimeField()
    time_open = models.DateTimeField()
    time_period_end = models.DateTimeField()
    time_period_start = models.DateTimeField()
    class Meta:
        db_table = 'coin_prices'


class CurrentPrices(models.Model):
    """
    Stores the most recent information on coin prices
    """
    id = models.AutoField(primary_key=True)
    coin = models.OneToOneField(Coins, on_delete=models.CASCADE, unique=True)
    rate_close = models.DecimalField(max_digits=24, decimal_places=11)
    rate_open = models.DecimalField(max_digits=24, decimal_places=11)
    time_period_start = models.DateTimeField()
    time_period_end = models.DateTimeField()
    class Meta:
        db_table = 'current_prices'
