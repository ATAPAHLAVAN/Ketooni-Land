from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_name', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'customer_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'customer_name', 'phone', 'address')
        }),
        ('اطلاعات سفارش', {
            'fields': ('total_price', 'status')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('order__created_at', 'product')
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('price',)