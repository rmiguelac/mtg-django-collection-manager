from django.db import models


class Card(models.Model):

    owner = models.ForeignKey('auth.User', related_name='cards', on_delete=models.CASCADE)
    name = models.CharField('Card Name', max_length=128, db_index=True)
    expansion = models.CharField('Expansion', max_length=64, blank=True)
    condition = models.CharField('Condition', max_length=2, blank=True)
    foil = models.BooleanField('Foil', default=False, null=True)
    quantity = models.IntegerField('Quantity', default=1)
    value = models.DecimalField('Value', max_digits=6, decimal_places=2, blank=True, default=0.00)

    class Meta:
        unique_together = ('name', 'expansion', 'condition', 'foil')

    def __str__(self):
        return f'{self.name}'
