from django.db import models
from coins.models import Coins


class ArticleAggregates(models.Model):
    """
    Hourly totals of articles from sources.
    """
    id = models.AutoField(primary_key=True)
    coin = models.ForeignKey(Coins, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    count = models.IntegerField()

    class Meta:
        db_table = 'article_aggregates'
        unique_together = ('coin', 'start_time', 'end_time',)


class Platforms(models.Model):
    """
    Lookup of the platforms on which articles are published
    ie. twitter, bbc etc
    """
    id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=64)
    impact = models.IntegerField()

    class Meta:
        db_table = 'platforms'
