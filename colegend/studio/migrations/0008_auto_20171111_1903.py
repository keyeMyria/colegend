# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0007_auto_20171111_1849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['-created'], 'verbose_name': 'Chapter', 'verbose_name_plural': 'Chapters'},
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='name'),
        ),
    ]
