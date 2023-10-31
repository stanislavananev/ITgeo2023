from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3)


class HistoricalExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.currency.code} - {self.exchange_rate} at {self.timestamp}"
