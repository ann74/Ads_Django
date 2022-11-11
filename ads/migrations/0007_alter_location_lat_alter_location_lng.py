# Generated by Django 4.1.3 on 2022-11-10 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_alter_location_lat_alter_location_lng'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.DecimalField(decimal_places=6, max_digits=8, null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='location',
            name='lng',
            field=models.DecimalField(decimal_places=6, max_digits=8, null=True, verbose_name='Долгота'),
        ),
    ]