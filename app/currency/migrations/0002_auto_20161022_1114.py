# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplier',
            name='rate',
            field=models.DecimalField(decimal_places=4, max_digits=25),
        ),
    ]