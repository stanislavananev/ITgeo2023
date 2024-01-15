from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)


class UserPortfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usd_balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    eur_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gbp_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    jpy_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username


class Currency(models.Model):
    code = models.CharField(max_length=3)


class HistoricalExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.currency.code} - {self.exchange_rate} at {self.timestamp}"
