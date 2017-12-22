# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 16:13
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0008_auto_20171204_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating'),
        ),
    ]