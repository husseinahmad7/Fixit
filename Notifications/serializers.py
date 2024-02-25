# serializers.py
from rest_framework import serializers
from .models import Notification
from Ticket.serializers import TicketSerializer
class NotificationSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()
    title = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.get_title_body()[0]

    def get_body(self, obj):
        return obj.get_title_body()[1]
    class Meta:
        model = Notification
        fields = ['id', 'ticket', 'user', 'type', 'date','title','body', 'is_seen']