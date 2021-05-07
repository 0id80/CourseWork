from django.db import models


class Iteration(models.Model):
    percent = models.PositiveSmallIntegerField(verbose_name="Percent")
    iteration_number = models.FloatField(verbose_name="Iteration number", primary_key=True)
    scheme = models.TextField(verbose_name="Scheme")
    disk_in_motion = models.PositiveIntegerField(verbose_name="Disk in motion", null=True, blank=True)
