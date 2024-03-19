from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_title', 'date', 'is_seen')
    list_filter = ('is_seen',)
    search_fields = ('user__email', 'user__full_name', 'ticket__client__full_name')
    ordering = ('-date',)
    readonly_fields = ('date',)  # Mark date as read-only

    def get_title(self, obj):
        return obj.get_title_body()[0]  # Display the title part of the notification
    get_title.short_description = 'Title'

admin.site.register(Notification, NotificationAdmin)