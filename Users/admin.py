from django.contrib import admin

# Register your models here.
# from django.contrib.auth.admin import UserAdmin
from .models import User,Staff

admin.site.register(User)
admin.site.register(Staff)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class StaffInline(admin.StackedInline):
#     model = Staff
#     can_delete = False
#     verbose_name_plural = "employee"


# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = [StaffInline]


# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)