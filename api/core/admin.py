from django.contrib import admin

from shop.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Custom category display in admin panel."""
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Custom product display in admin panel."""
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}