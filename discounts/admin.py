from django.contrib import admin
from .models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'value', 'times_used', 'max_uses', 'is_active', 'valid_to']
    list_filter = ['discount_type', 'is_active']
    search_fields = ['code']
