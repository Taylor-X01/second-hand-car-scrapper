# Generated by Django 3.2 on 2021-06-14 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csvs', '0004_alter_carpost_km'),
    ]

    operations = [
        migrations.AddField(
            model_name='carpost',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
