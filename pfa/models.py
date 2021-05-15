from django.db import models
from django.db.models.fields import CharField

class car_data(models.Model):
    # Object fields
    brand   = models.CharField(max_length=100)
    model   = models.CharField(max_length=50)
    year    = models.DecimalField()
    km_min  = models.DecimalField()
    km_max  = models.DecimalField()
    city    = models.CharField(max_length=50)