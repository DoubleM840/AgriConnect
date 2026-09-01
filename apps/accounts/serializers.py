from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import BuyerProfile, FarmerProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Read-only view of a user — used to show 'who am I' after login."""

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "role", "county", "date_joined")
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles new account creation. Password is write_only so it never
    round-trips back in a response. We use Django's own password
    validators (length, similarity, common-password checks) rather than
    reinventing that logic.
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "password", "role", "county")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Auto-create the matching profile so the frontend never has to
        # make a second request just to get a usable account.
        if user.role == User.Role.FARMER:
            FarmerProfile.objects.create(user=user)
        elif user.role == User.Role.BUYER:
            BuyerProfile.objects.create(user=user)

        return user