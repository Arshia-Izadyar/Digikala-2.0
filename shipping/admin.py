from django.contrib import admin

from .models import Shipping, ShippingItem


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ("user", "sending_date", "delivery_method")
    search_fields = ("user",)


@admin.register(ShippingItem)
class ShippingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")
    search_fields = ("product",)