from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'created_at']
    list_filter = ['role', 'is_verified']
    fieldsets = UserAdmin.fieldsets + (
        ('SEKANI Info', {'fields': ('role', 'phone', 'address', 'city', 'state', 'profile_picture', 'is_verified')}),
    )
