# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-12 16:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0003_auto_20170612_1811'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WaitingListItem',
            new_name='WaitingUser',
        ),
    ]
