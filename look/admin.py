from django.contrib import admin
from .models import Product, ProductIndex
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # List all the columns to display in the admin panel
    list_display = ('product_id', 'product_name', 'category', 'discounted_price', 
                    'actual_price', 'discount_percentage', 'rating', 'rating_count')
    # Add search functionality
    search_fields = ('product_name', 'category', 'product_id')
    # Add filtering options
    list_filter = ('category', 'discount_percentage', 'rating')

# Register the model and admin clas

@admin.register(ProductIndex)
class ProductAdmin(admin.ModelAdmin):
    # List all the columns to display in the admin panel
    list_display = ('product_id', 'name_tokens', 'categories', 'price', 
                    'discount_percentage', 'rating', 'rating_count')
    # Add search functionality
    search_fields = ('product_id', 'name_tokens', 'categories')
    # Add filtering options
    list_filter = ('categories', 'discount_percentage', 'rating')