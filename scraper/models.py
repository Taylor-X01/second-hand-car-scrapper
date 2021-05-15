from django.db import models

# Create your models here.

class car_data(models.Model):
    # Object fields
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.DecimalField(max_digits=16, decimal_places=2)
    km_min = models.DecimalField(max_digits=16, decimal_places=2)
    km_max = models.DecimalField(max_digits=16, decimal_places=2)
    city = models.CharField(max_length=50)
