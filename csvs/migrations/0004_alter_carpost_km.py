# Generated by Django 3.2 on 2021-06-14 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csvs', '0003_auto_20210613_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carpost',
            name='km',
            field=models.TextField(),
        ),
    ]
