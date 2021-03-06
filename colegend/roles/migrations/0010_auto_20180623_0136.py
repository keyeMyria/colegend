# Generated by Django 2.0.4 on 2018-06-22 23:36

from django.db import migrations, models
import django.db.models.deletion


initial_circles_data = [
    {
        'name': 'Colegend',
    },
]


def create_initial_circles(apps, schema_editor):
    Circle = apps.get_model('roles', 'Circle')
    db_alias = schema_editor.connection.alias
    circles = []
    for data in initial_circles_data:
        circle = Circle(
            name=data.get('name'),
        )
        circles.append(circle)
    Circle.objects.using(db_alias).bulk_create(circles)


def delete_initial_circles(apps, schema_editor):
    Circle = apps.get_model('roles', 'Circle')
    db_alias = schema_editor.connection.alias
    Circle.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0009_auto_20180623_0100'),
    ]

    operations = [
        migrations.RunPython(create_initial_circles, delete_initial_circles),
        migrations.AddField(
            model_name='role',
            name='circle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='roles.Circle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('circle', 'name')},
        ),
    ]

