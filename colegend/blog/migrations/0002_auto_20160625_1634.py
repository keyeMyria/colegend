# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 14:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogtag',
            options={'verbose_name': 'Blog tag', 'verbose_name_plural': 'Blog tags'},
        ),
    ]
