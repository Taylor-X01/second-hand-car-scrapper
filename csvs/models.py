from django.db import models
from django.db.models.fields import IntegerField

class carPost(models.Model):
    url     = models.URLField(null=True)
    img     = models.URLField(null=True)
    model   = models.TextField(max_length=50)
    option  = models.TextField(max_length=100)
    price   = models.IntegerField()
    vendor  = models.TextField(max_length=100)
    year    = models.IntegerField()
    city    = models.TextField(max_length=50)
    main    = models.TextField(max_length=30)
    km      = models.TextField()
    carb    = models.TextField(max_length=30)
    trans   = models.TextField(max_length=30)


