# Generated by Django 5.1.4 on 2024-12-13 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bins', '0001_initial'),
        ('smart_bins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='bin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='bins.wastebin'),
        ),
        migrations.DeleteModel(
            name='Route',
        ),
        migrations.DeleteModel(
            name='WasteBin',
        ),
    ]
