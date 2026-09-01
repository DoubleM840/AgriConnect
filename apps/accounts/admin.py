from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import BuyerProfile, FarmerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "phone_number", "role", "county", "is_active", "date_joined")
    list_filter = ("role", "is_active", "county")
    search_fields = ("username", "phone_number", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("AgriConnect profile", {"fields": ("role", "phone_number", "phone_verified", "county")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("AgriConnect profile", {"fields": ("role", "phone_number")}),
    )


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "farm_name", "farm_location", "is_verified")
    list_filter = ("is_verified",)
    search_fields = ("user__username", "farm_name", "farm_location")


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "buyer_type", "delivery_address")
    list_filter = ("buyer_type",)
    search_fields = ("user__username", "delivery_address")