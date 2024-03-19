# serializers.py
from rest_framework import serializers
from .models import Notification
from Ticket.serializers import TicketListSerializer
from Ticket.decorators import query_debugger
from django.utils.decorators import method_decorator

@method_decorator(query_debugger,name='to_representation')
class NotificationSerializer(serializers.ModelSerializer):
    ticket = TicketListSerializer()
    title = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    
    def get_title(self, obj):
        user = self.context.get('request').user
        if not user.is_staff:
            return obj.get_title_body()[0]
        else:
            return 'Ticket in progress'

    def get_body(self, obj):
        user = self.context.get('request').user
        if not user.is_staff:
            return obj.get_title_body()[1]
        else:
            return 'There is a Ticket paid and must be work on'
        
    class Meta:
        model = Notification
        fields = ['id', 'ticket', 'user', 'type', 'date','title','body', 'is_seen']