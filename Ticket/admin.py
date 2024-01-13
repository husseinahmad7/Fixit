from django.contrib import admin
from .models import Ticket, TicketPicture,ServiceCategory, Service
# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketPicture)
admin.site.register(ServiceCategory)
admin.site.register(Service)
