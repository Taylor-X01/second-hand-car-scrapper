from django.db import models
import django.db.models.fields

class car_data(models.Model):
    # Object fields
    brand   = models.CharField()
    model   = models.CharField()
    year    = models.DecimalField()
    km_min  = models.DecimalField()
    km_max  = models.DecimalField()
    city    = models.CharField()