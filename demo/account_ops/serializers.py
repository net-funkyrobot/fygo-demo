from rest_framework import serializers
from .constants import DECIMAL_KWARGS
from .models import Account, Transaction


class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["balance"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["transaction_id", "amount", "created"]


class TransactionWebhookSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    transaction_id = serializers.IntegerField()
    amount = serializers.DecimalField(**DECIMAL_KWARGS)
    created = serializers.DateTimeField()
