# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-05 14:52
from __future__ import unicode_literals

import colegend.cms.models
from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('home', '0003_auto_20170114_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(colegend.cms.models.UniquePageMixin, 'wagtailcore.page'),
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='content',
        ),
    ]
