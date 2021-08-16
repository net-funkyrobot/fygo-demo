from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.db.models.query import prefetch_related_objects
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny

from .models import Account, Transaction, WithdrawalRequest
from .serializers import (
    AccountBalanceSerializer,
    TransactionSerializer,
    TransactionWebhookSerializer,
    WithdrawalRequestSerializer,
)


class BalanceAPIView(RetrieveAPIView):
    queryset = Account.objects.all().prefetch_related("withdrawal_requests")
    serializer_class = AccountBalanceSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            id=self.request.user.account.id,
        )


class TransactionsAPIView(ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            account_id=self.request.user.account.id,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def transaction_create_webhook_api_view(request):
    serializer = TransactionWebhookSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        user_model = get_user_model()
        user = get_object_or_404(
            user_model.objects.all().prefetch_related("account"),
            id=data["user_id"],
        )

        Transaction.objects.create(
            account_id=user.account.id,
            transaction_id=data["transaction_id"],
            amount=data["amount"],
            created=data["created"],
        )
        Account.objects.update(
            user_id=user.id,
            internal_balance=F("internal_balance") + data["amount"],
        )
        return Response("OK")


@api_view(["POST"])
@transaction.atomic
def create_withdrawal_request(request):
    serializer = WithdrawalRequestSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        account = Account.objects.prefetch_related("withdrawal_requests").get(
            id=request.user.account.id
        )

        if account.balance - data["amount"] >= Decimal(0):
            WithdrawalRequest.objects.create(
                account_id=account.id,
                amount=data["amount"],
            )
            return Response("OK")

    return Response(status=400)
