# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0006_auto_20171111_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
    ]
