# Generated by Django 3.0.2 on 2020-01-09 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concierge', '0005_auto_20200109_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='apartment',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='tenant',
        ),
        migrations.DeleteModel(
            name='Apartment',
        ),
        migrations.DeleteModel(
            name='Journal',
        ),
        migrations.DeleteModel(
            name='Tenant',
        ),
    ]
