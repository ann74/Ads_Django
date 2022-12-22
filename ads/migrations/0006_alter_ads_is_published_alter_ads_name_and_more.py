# Generated by Django 4.1.3 on 2022-12-04 09:21

import ads.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_alter_categories_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='is_published',
            field=models.BooleanField(validators=[ads.models.not_published], verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='ads',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='Тема'),
        ),
        migrations.AlterField(
            model_name='ads',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость'),
        ),
    ]