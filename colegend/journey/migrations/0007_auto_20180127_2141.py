# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-27 20:41
from __future__ import unicode_literals

import colegend.core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0006_auto_20180127_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demon',
            name='content',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
        migrations.AlterField(
            model_name='hero',
            name='content',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
    ]