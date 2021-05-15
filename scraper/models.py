from django.db import models

# Create your models here.

class car_data(models.Model):
    # Object fields
    brand   = models.CharField(max_length=50)
    model   = models.CharField(max_length=50)
    year    = models.DecimalField(max_digits=16, decimal_places=0)
    km      = models.DecimalField(max_digits=16, decimal_places=0)
    city    = models.CharField(max_length=50)
    price   = models.DecimalField(null='true',max_digits=10,decimal_places=0)
    url = models.CharField(max_length=100,blank='false', null='false')
