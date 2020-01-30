# Generated by Django 3.0.2 on 2020-01-20 18:54

from django.db import migrations

OBJECTS_TO_CREATE = 5


def combine_names(apps, schema_editor):
    Tenant = apps.get_model('mycore', 'Tenant')
    Room = apps.get_model('mycore', 'Room')
    for i in range(OBJECTS_TO_CREATE):
        room = Room(number=i)
        tenant = Tenant(first_name=f'test_first_{i}',
                        last_name=f'test_last_{i}')
        room.tenant = tenant
        tenant.save()
        room.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mycore', '0002_journal_room'),
    ]

    operations = [
        migrations.RunPython(combine_names)
    ]
