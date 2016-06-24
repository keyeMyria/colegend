# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 07:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.tag',),
        ),
        migrations.AlterField(
            model_name='blogarticlepage',
            name='date',
            field=models.DateField(default=datetime.date(2016, 6, 23), help_text='This date may be displayed on the blog article. It is not used to schedule posts to go live at a later date.', verbose_name='Display date'),
        ),
    ]