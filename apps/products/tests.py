from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.products.models import Category, Product


class ProductPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # ✅ UNIQUE PHONE NUMBERS ARE MANDATORY FOR YOUR USER MODEL
        self.farmer = User.objects.create_user(
            username="farmer", 
            password="pass", 
            role=User.Role.FARMER,
            phone_number="+254700000001"  # <-- CRITICAL FIX
        )
        self.buyer = User.objects.create_user(
            username="buyer", 
            password="pass", 
            role=User.Role.BUYER,
            phone_number="+254700000002"  # <-- CRITICAL FIX
        )
        self.category = Category.objects.create(name="Veg", slug="veg")
        self.product_url = "/api/products/products/"

    def test_farmer_can_create_product(self):
        self.client.force_authenticate(user=self.farmer)
        data = {
            "name": "Carrots",
            "category": self.category.id,
            "price_per_unit": "50.00",
            "quantity_available": "100.00",
            "county": "Nyeri",
            "unit": "CRATE",  # ✅ CHANGED FROM "kg" TO VALID CHOICE
            "harvest_date": "2026-09-01",
            "is_active": True,
            "description": "Fresh carrots"
        }
        response = self.client.post(self.product_url, data, format="json")
        
        if response.status_code != 201:
            print(f"ERROR: {response.status_code}")
            print(f"RESPONSE: {response.json()}")
            
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

    def test_buyer_cannot_create_product(self):
        self.client.force_authenticate(user=self.buyer)
        data = {
            "name": "Bananas", 
            "category": self.category.id, 
            "price_per_unit": "10.00",
            "quantity_available": "50.00",
            "county": "Nyeri",
            "unit": "kg",
            "harvest_date": "2026-09-01",
            "is_active": True
        }
        response = self.client.post(self.product_url, data, format="json")
        self.assertEqual(response.status_code, 403)