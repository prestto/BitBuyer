from django.db import models

class Coins(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=31)
    abbreviation = models.CharField(max_length=7, unique=True)
    description = models.CharField(max_length=3000)
    icon = models.CharField(max_length=27)

    class Meta:
        db_table = 'coins'
