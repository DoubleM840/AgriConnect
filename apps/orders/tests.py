from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.products.models import Category, Product
from apps.orders.models import Order


class OrderCreationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # ✅ UNIQUE PHONE NUMBERS
        self.buyer = User.objects.create_user(
            username="buyer", 
            password="pass", 
            role=User.Role.BUYER,
            phone_number="+254700000003"  # <-- ADDED
        )
        self.farmer = User.objects.create_user(
            username="farmer", 
            password="pass", 
            role=User.Role.FARMER,
            phone_number="+254700000004"  # <-- ADDED
        )
        self.category = Category.objects.create(name="Fruit", slug="fruit")
        self.product = Product.objects.create(
            name="Apples", farmer=self.farmer, category=self.category,
            price_per_unit="100.00", quantity_available="50.00", county="Nyeri", unit="kg"
        )
        self.order_url = "/api/orders/orders/"

    def test_create_order_deducts_stock(self):
        self.client.force_authenticate(user=self.buyer)
        data = {
            "delivery_address": "123 Main St",
            "items": [{"product": str(self.product.id), "quantity": "5.00"}]
        }
        response = self.client.post(self.order_url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity_available, 45.00)

    def test_insufficient_stock_fails(self):
        self.client.force_authenticate(user=self.buyer)
        data = {
            "delivery_address": "123 Main St",
            "items": [{"product": str(self.product.id), "quantity": "999.00"}]
        }
        response = self.client.post(self.order_url, data, format="json")
        self.assertEqual(response.status_code, 400)