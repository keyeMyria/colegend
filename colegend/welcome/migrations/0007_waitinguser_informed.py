# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-12 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0006_waitinguser_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinguser',
            name='informed',
            field=models.BooleanField(default=False),
        ),
    ]
