from rest_framework import serializers
from .models import Ticket, ServiceCategory, Service, TicketPicture
from Users.models import User
def imort_userserializer():
    from Users.serializers import UserSerializer
    return UserSerializer

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'title','icon']


class ServiceSerializer(serializers.ModelSerializer):
    service_category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'initial_price', 'service_category','picture','type','is_final_price']

class TicketPictureSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = TicketPicture
        fields = ['id','ticket', 'picture']

class TicketSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Ticket
        fields = ['id', 'description', 'service','location','info_fields', 'assigned_to', 'status', 'client_rating', 'notes','final_price', 'submission_date', 'workers']
    def to_representation(self, instance):
        # Fetch the client details
        client = instance.client
        client_info = {
            'client_id': client.id,
            'email': client.email,
            'full_name': client.full_name,
            'mobile': client.mobile,
            
        }

        # Combine the client info with other serialized fields
        representation = super().to_representation(instance)
        representation.update(client_info)
        return representation

class  TicketCreationSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    status = serializers.SerializerMethodField()
    pictures = serializers.ManyRelatedField(child_relation=TicketPictureSerializer(),read_only=True)
    class Meta:
        model = Ticket
        fields = ['client', 'description', 'service','location','info_fields','status','client_rating', 'pictures']
    def get_status(self, obj):
        return obj.status
    def validate_client_rating(self, value):
        ticket = self.instance
        if ticket.status != 'Closed' and value is not None:
            raise serializers.ValidationError("Client rating can only be updated when the ticket is closed.")
        return value

class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['client','status','client_rating']

    def validate_client_rating(self, value):
        ticket = self.instance
        if ticket.status != 'Closed' and value is not None:
            raise serializers.ValidationError("Client rating can only be updated when the ticket is closed.")
        return value


class StaffTicketDetailsSerializer(serializers.ModelSerializer):
    
    service = ServiceSerializer()
    pictures = serializers.ManyRelatedField(child_relation=TicketPictureSerializer(),read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'description', 'service','location','info_fields', 'assigned_to', 'status', 'client_rating', 'notes','final_price', 'submission_date', 'workers','pictures']
        read_only_fields = ['id', 'client', 'description', 'service','location','info_fields', 'assigned_to', 'status', 'client_rating','final_price', 'submission_date', 'workers','pictures']
    def to_representation(self, instance):
        # Fetch the client details
        client = instance.client
        client_info = {
            'client_id': client.id,
            'email': client.email,
            'full_name': client.full_name,
            'mobile': client.mobile,
            
        }

        # Combine the client info with other serialized fields
        representation = super().to_representation(instance)
        representation.update(client_info)
        return representation

class StaffTicketStatusSerializer(serializers.ModelSerializer):
    # workers = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['assigned_to','final_price', 'workers']
        read_only_fields = ['workers']

    def validate_final_price(self, value):
        """
        Validate the final_price based on the is_final_price flag of the ticket service.
        """
        ticket = self.instance  # Get the ticket instance being updated
        service = ticket.service

        if service.is_final_price:
            # If the service has is_final_price set to True, ensure the final_price matches the service price
            if value != service.initial_price:
                return service.initial_price
        return value