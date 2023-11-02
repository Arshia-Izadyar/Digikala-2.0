from django.contrib import admin

from .models import Transactions, Wallet


@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "type", "created_at", "invoice_number")
    fields = ("user", "amount", "type", "basket", "invoice_number")
    search_fields = ("invoice_number", "user")


@admin.register(Wallet)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total")
    fields = ("user", "total")
    search_fields = ("user",)
    