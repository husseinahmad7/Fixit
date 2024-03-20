# serializers.py
from rest_framework import serializers
from .models import Notification
from Ticket.serializers import TicketListSerializer
# from Ticket.decorators import query_debugger
# from django.utils.decorators import method_decorator

# @method_decorator(query_debugger,name='to_representation')
class NotificationSerializer(serializers.ModelSerializer):
    ticket = TicketListSerializer()
    title = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    
    def get_title(self, obj):
        user = self.context.get('request').user
        if  user.is_staff and user.staff.is_supervisor==False:
            return 'Ticket in progress'
        
        return obj.get_title_body()[0]

    def get_body(self, obj):
        user = self.context.get('request').user
        if user.is_staff and user.staff.is_supervisor==False:
            return 'There is a Ticket paid and must be work on'
        return obj.get_title_body()[1]
        
    class Meta:
        model = Notification
        fields = ['id', 'ticket', 'user', 'type', 'date','title','body', 'is_seen']


class NotificationSeenActSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Notification
        fields = ['is_seen']