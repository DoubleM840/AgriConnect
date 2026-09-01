from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description")


class ProductSerializer(serializers.ModelSerializer):
    """
    farmer is read-only here — it's set automatically from the logged-in
    user in the view (perform_create), never taken from client input.
    That stops one farmer from creating listings under another farmer's name.
    """

    farmer = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "farmer", "category", "category_name", "name", "description",
            "unit", "price_per_unit", "quantity_available", "county",
            "harvest_date", "is_active", "is_in_stock", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")