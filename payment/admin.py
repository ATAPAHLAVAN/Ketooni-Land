from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user', 'order')
        }),
        ('اطلاعات پرداخت', {
            'fields': ('amount', 'status')
        }),
        ('اطلاعات تراکنش', {
            'fields': ('transaction_id', 'authority')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )