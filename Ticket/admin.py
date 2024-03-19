from django.contrib import admin
from .models import ServiceCategory, Service, Ticket

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_category', 'initial_price', 'type', 'is_final_price')
    list_filter = ('service_category', 'type', 'is_final_price')
    search_fields = ('title', 'description')
    ordering = ('title',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'status', 'assigned_to', 'submission_date')
    list_filter = ('status', 'assigned_to')
    search_fields = ('client__email', 'service__title', 'description')
    ordering = ('-submission_date',)
    readonly_fields = ('submission_date',)  # Mark submission_date as read-only

    fieldsets = (
        ('General Information', {
            'fields': ('client', 'service', 'status', 'assigned_to', 'submission_date')
        }),
        ('Additional Details', {
            'fields': ('description', 'location', 'info_fields', 'client_rating', 'notes', 'final_price', 'workers', 'paycode')
        }),
    )


admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Ticket, TicketAdmin)