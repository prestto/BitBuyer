from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=31)),
                ('abbreviation', models.CharField(max_length=7, unique=True)),
                ('description', models.CharField(max_length=10000)),
                ('icon', models.CharField(max_length=27)),
            ],
            options={
                'db_table': 'coins',
            },
        ),
        migrations.CreateModel(
            name='CoinPrices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rate_close', models.DecimalField(decimal_places=11, max_digits=24)),
                ('rate_high', models.DecimalField(decimal_places=11, max_digits=24)),
                ('rate_low', models.DecimalField(decimal_places=11, max_digits=24)),
                ('rate_open', models.DecimalField(decimal_places=11, max_digits=24)),
                ('time_close', models.DateTimeField()),
                ('time_open', models.DateTimeField()),
                ('time_period_end', models.DateTimeField()),
                ('time_period_start', models.DateTimeField()),
                ('coin', models.ForeignKey(on_delete=models.deletion.CASCADE, to='coins.coins')),
            ],
            options={
                'db_table': 'coin_prices',
            },
        ),
        migrations.CreateModel(
            name='CurrentPrices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rate_close', models.DecimalField(decimal_places=11, max_digits=24)),
                ('rate_open', models.DecimalField(decimal_places=11, max_digits=24)),
                ('time_period_start', models.DateTimeField()),
                ('time_period_end', models.DateTimeField()),
                ('coin', models.OneToOneField(on_delete=models.deletion.CASCADE, to='coins.coins')),
            ],
            options={
                'db_table': 'current_prices',
            },
        ),
    ]
