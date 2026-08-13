from django.contrib import admin
from .models import UserProfile, Address

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'city', 'is_default', 'created_at')
    list_filter = ('is_default', 'created_at', 'city')
    search_fields = ('user__username', 'city', 'title')
    readonly_fields = ('created_at',)