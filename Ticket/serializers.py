from rest_framework import serializers
from .models import Ticket, ServiceCategory, Service, TicketPicture
from Users.models import User
# from Users.serializers import StaffSerializer

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'title','icon']


class ServiceSerializer(serializers.ModelSerializer):
    service_category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'initial_price', 'service_category','picture','type']

class TicketPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPicture
        fields = ['id','ticket', 'picture']

class TicketSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = ['id', 'client','title', 'description', 'service', 'approved', 'assigned_to', 'status', 'client_rating', 'notes', 'is_paid', 'submission_date', 'workers']

class  TicketCreationSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    status = serializers.SerializerMethodField()
    # pictures = serializers.ManyRelatedField(child_relation=TicketPictureSerializer(),read_only=True)
    class Meta:
        model = Ticket
        fields = ['client','title', 'description', 'service','status','client_rating']
    def get_status(self, obj):
        return obj.status
    def validate_client_rating(self, value):
        ticket = self.instance
        if ticket.status != 'Closed' and value is not None:
            raise serializers.ValidationError("Client rating can only be updated when the ticket is closed.")
        return value

class StaffTicketSerializer(serializers.ModelSerializer):
    # workers = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['approved', 'assigned_to', 'status', 'notes', 'is_paid', 'workers']
        read_only_fields = ['workers']
