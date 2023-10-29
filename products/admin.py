from django.contrib import admin

from .models import Provider, Product, Category, Review


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', "provider_name", "working_perm_id", "joined")
    fields = ('user', "provider_name", "working_perm_id", "address", )
    
    search_fields = (
        "provider_name",
        "user",
    )
    ordering = ("joined",)


@admin.register(Product)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', "pid", "title", "price", )
    fields = ("pid", "title", "price", "description", "in_digikala_inventory", "in_provider_inventory", "provider", "category")
    
    search_fields = (
        "id",
        "title",
    )
    ordering = ("title",)


@admin.register(Category)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent", "slug")
    fields = ("title", "parent", "slug")
    
    search_fields = (
        "id",
        "title",
    )
    ordering = ("title",)

@admin.register(Review)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "rating", "product", "created_date")
    fields = ("user","rating", "product", "review", "recommend", "is_anon")
    
    search_fields = (
        "id",
    )
