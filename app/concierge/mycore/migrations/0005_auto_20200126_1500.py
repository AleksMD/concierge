# Generated by Django 3.0.1 on 2020-01-26 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycore', '0004_auto_20200126_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={},
        ),
        migrations.AlterModelOptions(
            name='tenant',
            options={'ordering': ['first_name', 'last_name']},
        ),
    ]
