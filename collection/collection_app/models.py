from django.db import models


class Cards(models.Model):

    name = models.CharField('Card Name', max_length=128)
    set = models.CharField('Set', max_length=64, blank=True)
    condition = models.CharField('Condition', max_length=2, blank=True)
    foil = models.BooleanField('Foil', default=False)
    quantity = models.IntegerField('Quantity', default=1)
    value = models.FloatField('Value quantity value', default=0.00)

    def __str__(self):
        return f'{self.name}'

