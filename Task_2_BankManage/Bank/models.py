from django.db import models


class Person(models.Model):
    name = models.CharField(verbose_name="Name", max_length=20, unique=True)
    money = models.DecimalField(verbose_name="Money", max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name