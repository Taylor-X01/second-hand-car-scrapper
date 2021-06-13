from django.db import models
from django.db.models.fields import IntegerField

class carPost_wandaloo(models.Model):
    model   = models.TextField(max_length=50)
    # option  = models.TextField(max_length=100)
    price   = models.IntegerField()
    vendor  = models.TextField(max_length=100)
    # tel     = models.TextField(max_length=13)
    year    = models.IntegerField()
    city    = models.TextField(max_length=50)
    main    = models.TextField(max_length=30)
    km      = models.IntegerField()
    carb    = models.TextField(max_length=30)
    trans   = models.TextField(max_length=30)


class carPost_moteur(models.Model):
    model = models.TextField(max_length=50)
    price = models.IntegerField()
    vendor = models.TextField(max_length=100)
    year = models.IntegerField()
    km = models.IntegerField()
    carb = models.TextField(max_length=30)
    trans = models.TextField(max_length=30)
