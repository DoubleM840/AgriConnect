from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for AgriConnect."""

    class UserType(models.TextChoices):
        FARMER = "farmer", "Farmer"
        BUYER = "buyer", "Buyer"

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.FARMER,
    )
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="farmer_profile")
    farm_location = models.CharField(max_length=255)
    farm_size_acres = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    crops_grown = models.TextField(blank=True)

    def __str__(self):
        return f"Farmer Profile: {self.user.username}"


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="buyer_profile")
    company_name = models.CharField(max_length=255, blank=True)
    preferred_categories = models.TextField(blank=True)

    def __str__(self):
        return f"Buyer Profile: {self.user.username}"