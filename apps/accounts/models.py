import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        FARMER = "FARMER", "Farmer"
        BUYER = "BUYER", "Buyer"
        ADMIN = "ADMIN", "Admin"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)
    phone_number = models.CharField(max_length=15, unique=True, help_text="E.164 format, e.g. +254712345678")
    phone_verified = models.BooleanField(default=False)
    county = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_farmer(self):
        return self.role == self.Role.FARMER

    @property
    def is_buyer(self):
        return self.role == self.Role.BUYER


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="farmer_profile")
    farm_name = models.CharField(max_length=150, blank=True)
    farm_location = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"FarmerProfile<{self.user.username}>"


class BuyerProfile(models.Model):
    class BuyerType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        RETAILER = "RETAILER", "Retailer"
        RESTAURANT = "RESTAURANT", "Restaurant"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="buyer_profile")
    buyer_type = models.CharField(max_length=15, choices=BuyerType.choices, default=BuyerType.INDIVIDUAL)
    delivery_address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"BuyerProfile<{self.user.username}>"