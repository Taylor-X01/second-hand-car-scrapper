# Generated by Django 3.2 on 2021-06-13 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csvs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carpost_moteur',
            name='km',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='carpost_moteur',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='carpost_moteur',
            name='year',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='carpost_wandaloo',
            name='km',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='carpost_wandaloo',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='carpost_wandaloo',
            name='year',
            field=models.IntegerField(),
        ),
    ]