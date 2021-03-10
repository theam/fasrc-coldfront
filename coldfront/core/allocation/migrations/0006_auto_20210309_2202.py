# Generated by Django 2.2.13 on 2021-03-10 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocation', '0005_auto_20210309_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocationuser',
            name='usage_bytes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='historicalallocationuser',
            name='usage_bytes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
