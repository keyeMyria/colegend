# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-28 23:51
from __future__ import unicode_literals

import colegend.core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0009_hero_bucket'),
    ]

    operations = [
        migrations.AddField(
            model_name='demon',
            name='tensions',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
    ]
