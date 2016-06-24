# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 16:37
from __future__ import unicode_literals

import colegend.cms.blocks
from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160623_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticlepage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField((('heading', colegend.cms.blocks.HeadingBlock()), ('rich_text', colegend.cms.blocks.RichTextBlock()), ('image', colegend.cms.blocks.ImageBlock()), ('embed', colegend.cms.blocks.EmbedBlock())), blank=True),
        ),
    ]
