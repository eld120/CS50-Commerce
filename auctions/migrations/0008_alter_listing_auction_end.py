# Generated by Django 3.2.12 on 2022-03-11 20:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_auction_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='auction_end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 18, 20, 32, 6, 161159, tzinfo=utc), null=True),
        ),
    ]
