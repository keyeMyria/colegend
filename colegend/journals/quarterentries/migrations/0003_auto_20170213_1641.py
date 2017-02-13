# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-13 15:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def backup_focus(apps, schema_editor):
    QuarterEntry = apps.get_model("quarterentries", "QuarterEntry")
    for entry in QuarterEntry.objects.all():
        if entry.content and entry.focus:
            entry.content = "Focus:\n{}\n\n{}".format(entry.focus, entry.content)
        entry.save()


class Migration(migrations.Migration):

    dependencies = [
        ('outcomes', '0008_auto_20160602_1833'),
        ('quarterentries', '0002_quarterentry_focus'),
    ]

    operations = [
        migrations.RunPython(backup_focus),
        migrations.RemoveField(
            model_name='quarterentry',
            name='focus',
        ),
        migrations.AddField(
            model_name='quarterentry',
            name='outcome_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_focus_1', to='outcomes.Outcome'),
        ),
        migrations.AddField(
            model_name='quarterentry',
            name='outcome_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_focus_2', to='outcomes.Outcome'),
        ),
        migrations.AddField(
            model_name='quarterentry',
            name='outcome_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_focus_3', to='outcomes.Outcome'),
        ),
        migrations.AddField(
            model_name='quarterentry',
            name='outcome_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_focus_4', to='outcomes.Outcome'),
        ),
    ]
