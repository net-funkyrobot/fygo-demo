from django.db import models
from django.conf import settings
from enum import Enum

# Specify in one place for consistency
DECIMAL_KWARGS = {"max_digits": 9, "decimal_places": 2}  # Max 1M-1


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    balance = models.DecimalField(**DECIMAL_KWARGS)


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    transaction_id = models.IntegerField()
    amount = models.DecimalField(**DECIMAL_KWARGS)
    created = models.DateTimeField()


class WithdrawalStatus(Enum):
    open = "Open"
    completed = "Completed"
    failed = "Failed"


class WithdrawalRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    amount = models.DecimalField(**DECIMAL_KWARGS)
    created = models.DateTimeField(auto_now_add=True)
    processed = models.CharField(
        max_length=10,
        choices=[(tag, tag.value) for tag in WithdrawalStatus],
        default=WithdrawalStatus.open,
    )
