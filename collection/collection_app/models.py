from django.db import models


class Cards(models.Model):

    name = models.CharField('Card Name', max_length=128)
    edition = models.CharField('Edition', max_length=64, blank=True)
    condition = models.CharField('Condition', max_length=2, blank=True)
    quantity = models.IntegerField()
    unit_value = models.FloatField('Single card value')
    value = models.FloatField('Whole quantity value')
    location = models.CharField('Position where stored', max_length=128, blank=True)

    def __str__(self):
        return f'{self.name}'

