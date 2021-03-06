# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 22:12
from __future__ import unicode_literals

import colegend.cms.blocks
import colegend.cms.models
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0028_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Documentation',
            },
            bases=(colegend.cms.models.UniquePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='DocumentationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.core.fields.StreamField((('heading', colegend.cms.blocks.HeadingBlock()), ('rich_text', colegend.cms.blocks.RichTextBlock()), ('image', colegend.cms.blocks.ImageBlock()), ('embed', colegend.cms.blocks.EmbedBlock())), blank=True)),
            ],
            options={
                'verbose_name_plural': 'Documentation pages',
                'verbose_name': 'Documentation page',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FAQPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'FAQ',
            },
            bases=(colegend.cms.models.UniquePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='SupportPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Support',
            },
            bases=(colegend.cms.models.UniquePageMixin, 'wagtailcore.page'),
        ),
    ]
