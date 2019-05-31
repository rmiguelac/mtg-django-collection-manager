from django.db import models


class Cards(models.Model):

    name = models.CharField('Card Name', max_length=128, primary_key=True, db_index=True)
    set = models.CharField('Set', max_length=64, blank=True)
    condition = models.CharField('Condition', max_length=2, blank=True)
    foil = models.BooleanField('Foil', default=False, null=True)
    quantity = models.IntegerField('Quantity', default=1)
    value = models.DecimalField('Value', max_digits=6, decimal_places=2, null=True, default=0.00)

    def __str__(self):
        return f'{self.name}'

