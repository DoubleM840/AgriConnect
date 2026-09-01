from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "farmer", "category", "price_per_unit",
        "unit", "quantity_available", "county", "is_active",
    )
    list_filter = ("category", "county", "is_active", "unit")
    search_fields = ("name", "farmer__username", "county")
    autocomplete_fields = ("farmer", "category")
    readonly_fields = ("id", "created_at", "updated_at")