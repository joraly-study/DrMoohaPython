from django.contrib import admin
from .models import Product, Category, Tag, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'created_at', 'customer_phone')
    list_filter = ('created_at',)
    search_fields = ('order_number', 'customer_name', 'customer_phone')
    inlines = [OrderItemInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at', 'is_deleted')
    list_filter = ('category', 'tags', 'is_deleted', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('tags',)
