from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class UserAuthIntegrationTest(TestCase):
    def test_auth_token_setup(self):
        client = APIClient()
        response = client.post(
            "/auth/token/",
            {"username": "testuser1", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 400, response.data)

        # Create user and ensure token is auto generated for new user
        User = get_user_model()
        new_user = User.objects.create_user(
            "testuser1",
            password="testpassword",
        )
        new_user_token = Token.objects.get(user_id=new_user.id)

        # Ensure that the token can be retrieved given the correct user and
        # password
        response = client.post(
            "/auth/token/",
            {"username": "testuser1", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(
            response.data,
            {"token": new_user_token.key},
        )
