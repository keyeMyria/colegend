# Generated by Django 2.0.4 on 2018-06-28 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0012_auto_20180628_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='is_circle',
        ),
        migrations.RemoveField(
            model_name='role',
            name='is_core',
        ),
        migrations.AddField(
            model_name='role',
            name='kind',
            field=models.CharField(choices=[('standard', 'standard'), ('core', 'core'), ('circle', 'circle')], default='standard', max_length=25),
        ),
        migrations.AlterField(
            model_name='role',
            name='parent',
            field=models.ForeignKey(blank=True, limit_choices_to={'kind': 'circle'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='roles.Role'),
        ),
    ]
