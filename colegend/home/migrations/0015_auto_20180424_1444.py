# Generated by Django 2.0.3 on 2018-04-24 12:44

import colegend.core.intuitive_duration.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20180424_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='duration',
            field=colegend.core.intuitive_duration.modelfields.IntuitiveDurationField(default='10m', verbose_name='duration'),
        ),
    ]
