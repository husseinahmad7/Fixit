from rest_framework import serializers
from .models import Ticket, ServiceCategory, Service, TicketPicture
from Users.models import User
from django.db.models import Avg
from django.utils.decorators import method_decorator
from .decorators import query_debugger

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'title','icon']


class ServiceSerializer(serializers.ModelSerializer):
    service_category = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'initial_price', 'service_category','picture','type','is_final_price','average_rating']
    
    def get_average_rating(self, obj):
        # Calculate the average rating for the service
        return obj.tickets.aggregate(Avg('client_rating')).get('client_rating__avg', None)

class TicketServiceSerializer(serializers.ModelSerializer):
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
        # Serialize detailed information about each worker
        workers_info = [{'id': worker.id,'user_id':worker.user.id, 'full_name': worker.user.full_name,'email':worker.user.email,'mobile':worker.user.mobile,'department':worker.department,'salary':worker.salary,'availability':worker.availability,'services':TicketServiceSerializer(worker.services.all(),many=True).data} for worker in instance.workers.all()]
        
        # Combine the client info with other serialized fields
        representation = super().to_representation(instance)
        representation.update(client_info)
        representation['workers'] = workers_info
        return representation
@method_decorator(query_debugger,name='to_representation')
class TicketListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Ticket
        fields = ['id', 'service', 'assigned_to', 'status','final_price', 'submission_date','client_rating']
    
class TicketClientDetailSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Ticket
        fields = ['id', 'description', 'service','location','info_fields', 'assigned_to', 'status', 'client_rating', 'notes','final_price', 'submission_date', 'workers','paycode']
    def to_representation(self, instance):
        # Fetch the client details
        client = instance.client
        client_info = {
            'client_id': client.id,
            'email': client.email,
            'full_name': client.full_name,
            'mobile': client.mobile,
            
        }
        # Serialize detailed information about each worker
        workers_info = [{'id': worker.id,'user_id':worker.user.id, 'full_name': worker.user.full_name,'email':worker.user.email,'mobile':worker.user.mobile,'department':worker.department,'salary':worker.salary,'availability':worker.availability,'services':ServiceSerializer(worker.services.all(),many=True).data} for worker in instance.workers.all()]
        
        # Combine the client info with other serialized fields
        representation = super().to_representation(instance)
        representation.update(client_info)
        representation['workers'] = workers_info
        return representation

class  TicketCreationSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    status = serializers.SerializerMethodField()
    pictures = serializers.ManyRelatedField(child_relation=TicketPictureSerializer(),read_only=True)
    class Meta:
        model = Ticket
        fields = ['client', 'description', 'service','location','info_fields','status','client_rating', 'pictures','paycode']
        read_only_fields = ['paycode']
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
        fields = ['client','status','client_rating','paycode']
        read_only_fields = ['paycode']

    def validate_client_rating(self, value):
        ticket = self.instance
        if ticket.status != 'Closed' and value is not None:
            raise serializers.ValidationError("Client rating can only be updated when the ticket is closed.")
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Client rating must be between 1 and 5.")
        return value

class TicketClosingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status','notes']
        read_only_fields = ['status']


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
        workers_info = [{'id': worker.id,'user_id':worker.user.id, 'full_name': worker.user.full_name,'email':worker.user.email,'mobile':worker.user.mobile,'department':worker.department,'salary':worker.salary,'availability':worker.availability,'services':ServiceSerializer(worker.services.all(),many=True).data} for worker in instance.workers.all()]

        # Combine the client info with other serialized fields
        representation = super().to_representation(instance)
        representation.update(client_info)
        representation['workers'] = workers_info
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