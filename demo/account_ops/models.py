from decimal import Decimal
from django.db import models
from django.conf import settings
from enum import Enum

from .constants import DECIMAL_KWARGS


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="account",
    )
    internal_balance = models.DecimalField(
        **DECIMAL_KWARGS,
        default=Decimal(0),
    )

    @property
    def balance(self) -> Decimal:
        """
        Returns balance minus any active withdrawal amount
        Note: use with prefetch_related to optimise queries
        """
        withdrawal = self.withdrawal_requests.filter(
            status=WithdrawalStatus.open,
        )
        if len(withdrawal) == 0:
            return self.internal_balance
        else:
            return self.internal_balance - withdrawal.amount


class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="transactions",
        null=True,
    )
    transaction_id = models.IntegerField()
    amount = models.DecimalField(**DECIMAL_KWARGS)
    created = models.DateTimeField()


class WithdrawalStatus(Enum):
    open = "Open"
    completed = "Completed"
    failed = "Failed"


class WithdrawalRequest(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="withdrawal_requests",
        null=True,
    )
    amount = models.DecimalField(**DECIMAL_KWARGS)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[(tag, tag.value) for tag in WithdrawalStatus],
        default=WithdrawalStatus.open,
    )
