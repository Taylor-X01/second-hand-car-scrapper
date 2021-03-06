# Generated by Django 3.2 on 2021-05-15 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_car_data_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_data',
            name='km',
            field=models.DecimalField(decimal_places=0, max_digits=16),
        ),
        migrations.AlterField(
            model_name='car_data',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10, null='true'),
        ),
        migrations.AlterField(
            model_name='car_data',
            name='year',
            field=models.DecimalField(decimal_places=0, max_digits=16),
        ),
    ]
