# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-10 08:15
from __future__ import unicode_literals

import annoying.fields
import colegend.core.fields
import colegend.core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20170810_1727'),
        ('journey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('owner', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='heroes', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('content', colegend.core.fields.MarkdownField()),
            ],
            options={
                'verbose_name_plural': 'Heroes',
                'verbose_name': 'Hero',
                'default_related_name': 'hero',
            },
            bases=(colegend.core.models.OwnedCheckMixin, models.Model),
        ),
    ]
