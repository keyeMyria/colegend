# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 20:56
from __future__ import unicode_literals

from django.db import migrations

initial_roles_data = [
    {
        'name': 'Software Manager',
        'nickname': 'Nerd',
        'item': 'chip',
        'description': 'Administrator',
    },
    {
        'name': 'CEO',
        'nickname': 'Pilot',
        'item': 'baton',
        'description': '',
    },
    {
        'name': 'COO',
        'nickname': 'coPilot',
        'item': 'metronome',
        'description': '',
    },
    {
        'name': 'Core Manager',
        'nickname': 'Insider',
        'item': 'mantle',
        'description': '',
    },
    {
        'name': 'Facilitator',
        'nickname': 'Meeting Master',
        'item': 'marble',
        'description': '',
    },
    {
        'name': 'Guide',
        'nickname': 'Cloud Guide',
        'item': 'cloud',
        'description': '',
    },
    {
        'name': 'Content Manager',
        'nickname': 'Steward',
        'item': 'tray',
        'description': '',
    },
    {
        'name': 'Happiness Manager',
        'nickname': '',
        'item': 'Harp',
        'description': '',
    },
    {
        'name': 'Supporter',
        'nickname': 'Support Fairy',
        'item': 'Wand',
        'description': '',
    },
    {
        'name': 'Business Manager',
        'nickname': 'Treasure Master',
        'item': 'Coin',
        'description': '',
    },
]


def create_initial_roles(apps, schema_editor):
    Role = apps.get_model('roles', 'Role')
    db_alias = schema_editor.connection.alias
    roles = []
    for data in initial_roles_data:
        role = Role(
            name=data.get('name'),
            nickname=data.get('nickname'),
            # item=data.get('item'),
            description=data.get('description'),
        )
        roles.append(role)
    Role.objects.using(db_alias).bulk_create(roles)


def delete_initial_roles(apps, schema_editor):
    Role = apps.get_model('roles', 'Role')
    db_alias = schema_editor.connection.alias
    Role.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('roles', '0003_role_item'),
    ]

    operations = [
        migrations.RunPython(create_initial_roles, delete_initial_roles),
    ]
