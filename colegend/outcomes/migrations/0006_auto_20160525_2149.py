# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-25 19:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outcomes', '0005_auto_20160524_2201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outcome',
            options={'ordering': ['-modified'], 'verbose_name': 'outcome', 'verbose_name_plural': 'outcomes'},
        ),
    ]
