from django.contrib import admin
from .models import ServiceCategory, Service, Ticket
from django.core.mail import send_mail

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_category', 'initial_price', 'type', 'is_final_price')
    list_filter = ('service_category', 'type', 'is_final_price')
    search_fields = ('title', 'description')
    ordering = ('title',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id','client', 'service', 'status', 'assigned_to', 'submission_date')
    list_filter = ('status', 'assigned_to')
    search_fields = ('client__email', 'service__title', 'description')
    ordering = ('-submission_date',)
    readonly_fields = ('submission_date',)

    fieldsets = (
        ('General Information', {
            'fields': ('client', 'service', 'status', 'assigned_to', 'submission_date')
        }),
        ('Additional Details', {
            'fields': ('description', 'location', 'info_fields', 'client_rating', 'notes', 'final_price', 'workers', 'paycode')
        }),
    )

    def send_notification_email(self, request, queryset):
        """
        Custom admin action to send email notifications to clients.
        """
        for ticket in queryset:
            if ticket.client:
                # Customize the email subject and content
                subject = f"Ticket Review: #{ticket.id}"
                message = f"Dear {ticket.client.full_name},\n\nYou may review Your ticket which has a status {ticket.status}."
                from_email = "admin@fixit.com"
                recipient_list = [ticket.client.email]

                # Send the email
                send_mail(subject, message, from_email, recipient_list)

        self.message_user(request, f"Notification emails sent to {queryset.count()} clients.")

    send_notification_email.short_description = "Send notification email to clients"

    actions = [send_notification_email]


admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Ticket, TicketAdmin)