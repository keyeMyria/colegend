# Generated by Django 2.0.4 on 2018-06-28 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0015_auto_20180628_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='circle',
            field=models.ForeignKey(blank=True, limit_choices_to={'kind': 'circle'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='roles.Role'),
        ),
    ]
