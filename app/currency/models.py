from __future__ import unicode_literals

from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=3)


class Multiplier(models.Model):
    currency_first = models.ForeignKey(Currency, related_name='currency_one')
    currency_second = models.ForeignKey(Currency, related_name='currency_second')
    rate = models.DecimalField(max_digits=25, decimal_places=2)

    class Meta:
        unique_together = ('currency_first', 'currency_second', )

    def get_row(self):
        return {self.currency_first.name: self.rate}
