from django.db import models

class EthereumAddress(models.Model):
    address = models.CharField(max_length=42)
    balance = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    transaction_count = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_contract = models.BooleanField(default=False)  # Nuevo campo

    def __str__(self):
        return self.address


