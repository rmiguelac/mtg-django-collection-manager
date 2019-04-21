from django.db import models


class Cards(models.Model):

    name = models.CharField('Card Name', max_length=128)
    edition = models.CharField('Edition', max_length=64)
    condition = models.CharField('Condition', max_lenghh=2)
    quantity = models.IntegerField()
    unit_value = models.FloatField('Single card value')
    value = models.FloatField('Whole quantity value')
    location = models.CharField('Position where stored', max_length=128)

    def __str__(self):
        return f'{self.quantity}x {self.edition}\'s {self.name} in {self.condition} condition, valued in {self.value}'

