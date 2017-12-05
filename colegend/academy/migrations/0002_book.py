# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 19:26
from __future__ import unicode_literals

import colegend.core.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('author', models.CharField(max_length=255, verbose_name='name')),
                ('image_url', models.URLField(blank=True, verbose_name='image url')),
                ('content', colegend.core.fields.MarkdownField()),
                ('featured', models.BooleanField(default=False)),
            ],
            options={
                'default_related_name': 'books',
                'ordering': ['name'],
            },
        ),
    ]