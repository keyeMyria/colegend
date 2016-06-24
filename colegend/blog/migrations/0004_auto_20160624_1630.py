# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 14:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160623_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogarticlepage',
            name='lead',
            field=models.TextField(blank=True, verbose_name='Display date'),
        ),
        migrations.AlterField(
            model_name='blogarticlepage',
            name='color',
            field=models.CharField(blank=True, choices=[('#f72e74', 'pink'), ('#FFAB40', 'orange'), ('#eede39', 'yellow'), ('#a8e141', 'green'), ('#6bdaed', 'cyan'), ('#3197d6', 'blue'), ('#ad86fc', 'purple'), ('#455A64', 'dark')], max_length=80, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='blogarticlepage',
            name='date',
            field=models.DateField(default=datetime.date(2016, 6, 24), help_text='This date may be displayed on the blog article. It is not used to schedule posts to go live at a later date.', verbose_name='Display date'),
        ),
    ]