from rest_framework import serializers
from django.db import transaction

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_name", "quantity", "unit_price", "subtotal")
        read_only_fields = ("id", "unit_price", "subtotal")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    buyer_username = serializers.CharField(source="buyer.username", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "buyer", "buyer_username", "status", "delivery_address",
            "notes", "items", "total_amount", "created_at", "updated_at"
        )
        read_only_fields = ("id", "buyer", "total_amount", "created_at", "updated_at")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item_data in items_data:
                product = item_data["product"]
                # Snapshot current price & validate stock
                if product.quantity_available < item_data["quantity"]:
                    raise serializers.ValidationError(
                        f"Insufficient stock for {product.name}. Available: {product.quantity_available}"
                    )
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data["quantity"],
                    unit_price=product.price_per_unit  # Price snapshot!
                )
                # Deduct stock
                product.quantity_available -= item_data["quantity"]
                product.save()
        return order