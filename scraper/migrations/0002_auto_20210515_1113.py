# Generated by Django 3.2 on 2021-05-15 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car_data',
            old_name='km_max',
            new_name='km',
        ),
        migrations.RemoveField(
            model_name='car_data',
            name='km_min',
        ),
    ]