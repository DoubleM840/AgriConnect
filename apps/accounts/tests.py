from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.models import User


class UserModelTest(TestCase):
    def test_farmer_property(self):
        user = User.objects.create_user(
            username="farmer1", password="pass123", role=User.Role.FARMER
        )
        self.assertTrue(user.is_farmer)
        self.assertFalse(user.is_buyer)

    def test_buyer_property(self):
        user = User.objects.create_user(
            username="buyer1", password="pass123", role=User.Role.BUYER
        )
        self.assertTrue(user.is_buyer)
        self.assertFalse(user.is_farmer)


class RegistrationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/accounts/register/"

    def test_register_farmer_success(self):
        data = {
            "username": "newfarmer",
            "email": "farmer@test.com",
            "password": "securepass123",
            "role": "FARMER",
            "phone_number": "+254700000000",
            "county": "Nyeri",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().role, "FARMER")

    def test_register_missing_role_fails(self):
        data = {"username": "norole", "email": "test@test.com", "password": "pass123"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)