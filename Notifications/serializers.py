# serializers.py
from rest_framework import serializers
from .models import Notification
from Ticket.serializers import TicketSerializer
from Ticket.decorators import query_debugger
from django.utils.decorators import method_decorator
@method_decorator(query_debugger,name='to_representation')
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