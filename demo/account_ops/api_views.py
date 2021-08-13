from django.conf import settings
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
def transaction_create_webhook_api_view(request):
    data = TransactionWebhookSerializer(request.data)
    if data.is_valid():
        user_model = get_user_model(settings.AUTH_USER_MODEL)
        user = get_object_or_404(user_model.objects.all(), id=data.user_id)

        with transaction.atomic():
            Transaction.objects.create(
                user=user,
                transaction_id=data.transaction_id,
                amount=data.amount,
                created=data.created,
            )
            Account.objects.update(
                user_id=user.id,
                balance=F("balance") + data.amount,
            )
            return Response("OK")
    raise Exception()  # todo: raise a 400 error here
