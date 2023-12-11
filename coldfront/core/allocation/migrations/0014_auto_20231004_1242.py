# Generated by Django 3.2.17 on 2023-10-04 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocation', '0013_allocationaccount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allocation',
            options={'ordering': ['project'], 'permissions': (('can_view_all_allocations', 'Can view all allocations'), ('can_review_allocation_requests', 'Can review allocation requests'), ('can_manage_invoice', 'Can manage invoice'))},
        ),
        migrations.AlterModelOptions(
            name='historicalallocation',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation', 'verbose_name_plural': 'historical allocations'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationattribute',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation attribute', 'verbose_name_plural': 'historical allocation attributes'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationattributechangerequest',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation attribute change request', 'verbose_name_plural': 'historical allocation attribute change requests'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationattributetype',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation attribute type', 'verbose_name_plural': 'historical allocation attribute types'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationattributeusage',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation attribute usage', 'verbose_name_plural': 'historical allocation attribute usages'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationchangerequest',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation change request', 'verbose_name_plural': 'historical allocation change requests'},
        ),
        migrations.AlterModelOptions(
            name='historicalallocationuser',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical allocation user', 'verbose_name_plural': 'historical Allocation User Status'},
        ),
        migrations.RemoveField(
            model_name='allocationuser',
            name='allocation_group_quota',
        ),
        migrations.RemoveField(
            model_name='allocationuser',
            name='allocation_group_usage_bytes',
        ),
        migrations.RemoveField(
            model_name='historicalallocationuser',
            name='allocation_group_quota',
        ),
        migrations.RemoveField(
            model_name='historicalallocationuser',
            name='allocation_group_usage_bytes',
        ),
        migrations.AlterField(
            model_name='historicalallocation',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationattribute',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationattributechangerequest',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationattributetype',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationattributeusage',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationchangerequest',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalallocationuser',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
