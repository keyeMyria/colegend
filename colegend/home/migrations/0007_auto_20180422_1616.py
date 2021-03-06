# Generated by Django 2.0.3 on 2018-04-22 14:16

import colegend.core.fields
import colegend.core.intuitive_duration.modelfields
import colegend.core.models
import colegend.scopes.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0006_auto_20171127_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('scope', colegend.scopes.models.ScopeField(choices=[('day', 'day'), ('week', 'week'), ('month', 'month'), ('year', 'year')], default='day', max_length=5, verbose_name='scope')),
                ('icon', models.CharField(max_length=255, verbose_name='icon')),
                ('content', colegend.core.fields.MarkdownField(verbose_name='content')),
                ('duration', colegend.core.intuitive_duration.modelfields.IntuitiveDurationField(blank=True, null=True, verbose_name='duration')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'habits',
            },
            bases=(colegend.core.models.OwnedCheckMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HabitReminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('time', models.DateField(verbose_name='date')),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to='home.Habit')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'reminders',
            },
            bases=(colegend.core.models.OwnedCheckMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HabitTrackEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_events', to='home.Habit')),
            ],
            options={
                'default_related_name': 'track_events',
            },
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('scope', colegend.scopes.models.ScopeField(choices=[('day', 'day'), ('week', 'week'), ('month', 'month'), ('year', 'year')], default='day', max_length=5, verbose_name='scope')),
                ('content', colegend.core.fields.MarkdownField(verbose_name='content')),
            ],
            options={
                'default_related_name': 'routines',
            },
            bases=(colegend.core.models.OwnedCheckMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RoutineHabit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Habit')),
                ('routine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Routine')),
            ],
            options={
                'ordering': ('routine', 'order'),
            },
        ),
        migrations.AddField(
            model_name='routine',
            name='habits',
            field=models.ManyToManyField(related_name='routines', through='home.RoutineHabit', to='home.Habit'),
        ),
        migrations.AddField(
            model_name='routine',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to=settings.AUTH_USER_MODEL),
        ),
    ]
