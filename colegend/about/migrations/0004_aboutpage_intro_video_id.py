# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0003_auto_20160703_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutpage',
            name='intro_video_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
