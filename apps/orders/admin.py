from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "buyer__username", "delivery_address")
    autocomplete_fields = ("buyer",)
    readonly_fields = ("id", "created_at", "updated_at", "total_amount")
    inlines = [OrderItemInline]