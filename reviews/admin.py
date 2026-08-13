# File: reviews/admin.py

from django.contrib import admin
from .models import Review, ReviewVote


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    list_editable = ('is_approved',)
    fields = ('product', 'user', 'rating', 'comment', 'is_approved', 'admin_reply')


@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'is_like', 'created_at')