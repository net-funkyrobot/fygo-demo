from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny

from .models import Account, Transaction
from .serializers import (
    AccountBalanceSerializer,
    TransactionSerializer,
    TransactionWebhookSerializer,
)


class BalanceAPIView(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountBalanceSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            user_id=self.request.user.id,
        )


class TransactionsAPIView(ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user_id=self.request.user.id)


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def transaction_create_webhook_api_view(request):
    serializer = TransactionWebhookSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        user_model = get_user_model()
        user = get_object_or_404(
            user_model.objects.all(),
            id=data["user_id"],
        )

        Transaction.objects.create(
            user=user,
            transaction_id=data["transaction_id"],
            amount=data["amount"],
            created=data["created"],
        )
        Account.objects.update(
            user_id=user.id,
            balance=F("balance") + data["amount"],
        )
        return Response("OK")
