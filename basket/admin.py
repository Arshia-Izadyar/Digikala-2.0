from django.contrib import admin
from .models import Basket, BasketLine

# Register your models here.
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "is_paid")
    fields = ("user", "is_paid")
    
@admin.register(BasketLine)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("id", "quantity", "product", "basket")
    fields = ("quantity", "product", "basket")