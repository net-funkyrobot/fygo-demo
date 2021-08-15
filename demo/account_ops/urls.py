from django.urls import path
from .api_views import (
    BalanceAPIView,
    TransactionsAPIView,
    create_withdrawal_request,
    transaction_create_webhook_api_view,
)


urlpatterns = [
    path("balance/", BalanceAPIView.as_view()),
    path("transactions/", TransactionsAPIView.as_view()),
    path("transactions-webhook/", transaction_create_webhook_api_view),
    path("request-withdrawal/", create_withdrawal_request),
]
