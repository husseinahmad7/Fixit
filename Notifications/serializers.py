# serializers.py
from rest_framework import serializers
from .models import Notification
from Ticket.serializers import TicketSerializer
class NotificationSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()
    class Meta:
        model = Notification
        fields = ['id', 'ticket', 'user', 'type', 'date', 'is_seen']