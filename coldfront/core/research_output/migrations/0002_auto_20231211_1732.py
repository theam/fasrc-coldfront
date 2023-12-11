# Generated by Django 3.2.17 on 2023-12-11 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research_output', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalresearchoutput',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical research output', 'verbose_name_plural': 'historical research outputs'},
        ),
        migrations.AlterField(
            model_name='historicalresearchoutput',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
