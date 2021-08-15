from datetime import datetime
from decimal import Decimal
from rest_framework.test import APIClient
from account_ops.models import Account, Transaction
from django.contrib.auth import get_user_model
from django.test import TestCase


class AccountOpsIntegrationTest(TestCase):
    def test_locked_down(self):
        client = APIClient()

        # Ensure authenticated access required
        response = client.get("/account/balance/")
        self.assertEqual(response.status_code, 401)

        response = client.get("/account/transactions/")
        self.assertEqual(response.status_code, 401)

        # Except transactions webhook
        User = get_user_model()
        user1 = User.objects.create_user("user1", password="testpassword")
        response = client.post(
            "/account/transactions-webhook/",
            {
                "user_id": user1.id,
                "transaction_id": 1,
                "amount": Decimal(1.5),
                "created": datetime.now(),
            },
        )
        self.assertEqual(response.status_code, 200)

        # Ensure non-destructive endpoints are locked down appropriately
        client.force_authenticate(user1)
        for endpoint in ("/account/balance/", "/account/transactions/"):
            response = client.post(endpoint)
            self.assertEqual(response.status_code, 405)
            response = client.put(endpoint)
            self.assertEqual(response.status_code, 405)
            response = client.patch(endpoint)
            self.assertEqual(response.status_code, 405)
            response = client.delete(endpoint)
            self.assertEqual(response.status_code, 405)

        # Ensure transactions-hook is POST only
        client.logout()
        endpoint = "/account/transactions-webhook/"
        response = client.get(endpoint)
        self.assertEqual(response.status_code, 405)
        response = client.put(endpoint)
        self.assertEqual(response.status_code, 405)
        response = client.patch(endpoint)
        self.assertEqual(response.status_code, 405)
        response = client.delete(endpoint)
        self.assertEqual(response.status_code, 405)
        response = client.head(endpoint)
        self.assertEqual(response.status_code, 405)

    def test_transactions_webhook(self):
        User = get_user_model()
        user1 = User.objects.create_user("user1", password="testpassword")
        account1 = Account.objects.get(user_id=user1.id)

        self.assertEqual(
            Transaction.objects.filter(account_id=user1.account.id).count(),
            0,
        )
        self.assertEqual(account1.balance, Decimal(0))

        client = APIClient()

        for i in range(25):
            response = client.post(
                "/account/transactions-webhook/",
                {
                    "user_id": user1.id,
                    "transaction_id": i,
                    "amount": Decimal(1.5),
                    "created": datetime.now(),
                },
            )
            self.assertEqual(response.status_code, 200, response.data)

        self.assertEqual(
            Transaction.objects.filter(account_id=user1.account.id).count(),
            25,
        )

        new_account1 = Account.objects.get(user_id=user1.id)

        self.assertEqual(
            new_account1.balance,
            Decimal(1.5 * 25),
            "Balance is incorrect",
        )

    def test_transactions_list(self):
        User = get_user_model()
        user1 = User.objects.create_user("user1", password="testpassword")

        self.assertEqual(
            Transaction.objects.filter(account_id=user1.account.id).count(),
            0,
        )

        client = APIClient()
        client.force_authenticate(user1)

        for i in range(25):
            response = client.post(
                "/account/transactions-webhook/",
                {
                    "user_id": user1.id,
                    "transaction_id": i,
                    "amount": Decimal(1.5),
                    "created": datetime.now(),
                },
            )
            self.assertEqual(response.status_code, 200, response.data)

        response = client.get("/account/transactions/")

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(response.data.get("count"), 25, response.data)
        self.assertContains(response, "next")
        self.assertEqual(
            len(response.data.get("results")),
            20,
            response.data,
        )  # page size is 20

    def test_balance(self):
        User = get_user_model()
        user1 = User.objects.create_user("user1", password="testpassword")

        client = APIClient()
        client.force_authenticate(user1)

        response = client.get("/account/balance/")
        self.assertEqual(
            response.data.get("balance"),
            Decimal(0.00),
            response.data,
        )

        for i in range(25):
            response = client.post(
                "/account/transactions-webhook/",
                {
                    "user_id": user1.id,
                    "transaction_id": i,
                    "amount": Decimal(1.5),
                    "created": datetime.now(),
                },
            )
            self.assertEqual(response.status_code, 200, response.data)

        response = client.get("/account/balance/")
        self.assertEqual(
            response.data.get("balance"),
            Decimal(37.50),
            response.data,
        )

    def test_create_withdrawal_request(self):
        User = get_user_model()
        user1 = User.objects.create_user("user1", password="testpassword")

        client = APIClient()
        client.force_authenticate(user1)

        response = client.get("/account/balance/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.get("balance"),
            Decimal(0.00),
            response.data,
        )

        response = client.post(
            "/account/request-withdrawal/",
            {"amount": "5.00"},
        )
        self.assertEqual(response.status_code, 400)

        response = client.post(
            "/account/transactions-webhook/",
            {
                "user_id": user1.id,
                "transaction_id": "1",
                "amount": Decimal(35.00),
                "created": datetime.now(),
            },
        )
        self.assertEqual(response.status_code, 200, response.data)

        response = client.post(
            "/account/request-withdrawal/",
            {"amount": "5.00"},
        )
        self.assertEqual(response.status_code, 200)
