from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Staff

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'mobile', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'full_name', 'mobile')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'mobile')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'mobile', 'password1', 'password2'),
        }),
    )

class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'salary', 'availability', 'is_supervisor')
    list_filter = ('department', 'availability', 'is_supervisor')
    search_fields = ('user__email', 'user__full_name', 'user__mobile')
    ordering = ('user__email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Staff, StaffAdmin)
