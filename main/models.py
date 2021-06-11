from django.contrib.gis.db import models

class Airport(models.Model):
    name = models.CharField(max_length=64)
    point = models.PointField()