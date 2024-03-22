from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from Users.permissins import IsSuperUser
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import Ticket, Service, ServiceCategory, TicketPicture
from .serializers import TicketSerializer, ServiceSerializer, ServiceCategorySerializer,TicketListSerializer,TicketClientDetailSerializer, TicketCreationSerializer,TicketPictureSerializer,TicketStatusSerializer,StaffTicketDetailsSerializer, StaffTicketStatusSerializer,TicketClosingSerializer
from Users.models import Staff
# from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import OwnerOrAdminPermission,TicketPictureOwnerOrAdminPermission,TicketOwnerPermission
from django.db.models import Avg
from Notifications.models import Notification
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# from .decorators import query_debugger

def generate_payment_code(length=8):
    import secrets
    import string
    # Define the characters to use for the payment code
    characters = string.ascii_letters + string.digits

    # Generate a random payment code of the specified length
    payment_code = ''.join(secrets.choice(characters) for _ in range(length))
    return payment_code


# reading categories
class ServiceCategoryList(generics.ListAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(3600*3))  # Cache for 3 hour
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ServiceCategoryCreate(generics.CreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsSuperUser]
    # parser_classes = []

class ServiceCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsSuperUser]


# Services
class ServiceList(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(3600*3))  # Cache for 3 hour
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ServiceCreate(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsSuperUser]

class ServiceRetrieve(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsSuperUser]

class ServiceListByCategory(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(3600*3))  # Cache for 3 hour
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        # Assuming you have a category ID passed as a query parameter (e.g., ?category_id=1)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return Service.objects.filter(service_category__id=category_id)
        else:
            # Return all services if no category ID is provided
            return Service.objects.all()

class ServiceListByRating(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    @method_decorator(cache_page(3600*3))  # Cache for 3 hour
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        # Calculate average rating for each service
        services = self.queryset.annotate(average_rating=Avg('tickets__client_rating'))
        # Exclude services with no ratings
        return services.exclude(average_rating__isnull=True).order_by('-average_rating')

# Ticket
class TicketCreate(generics.CreateAPIView):
    """
    API view for creating a ticket along with attached pictures.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketCreationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the ticket data
        ticket_instance = serializer.save()

        # Handle attached pictures
        pictures_data = self.request.FILES.getlist('pictures')  # 'pictures' is the field name
        for picture_data in pictures_data:
            TicketPicture.objects.create(ticket=ticket_instance, picture=picture_data)


class ClientTicketsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketListSerializer


    @method_decorator(cache_page(60*1))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    # @method_decorator(query_debugger)
    def get_queryset(self):
        user = self.request.user
        # Check if the 'filtered' parameter is set to 'true'
        filter_param = self.request.query_params.get('filtered','')
        if filter_param == 'true':
            # Customize the status values as needed 
            allowed_statuses = ['Open', 'In Progress', 'Pending Payment','Pending Approval','Closed']

            # Filter tickets based on the allowed statuses
            
            queryset = Ticket.objects.filter(client=user,status__in=allowed_statuses).prefetch_related('service')
            
            # queryset = Ticket.objects.filter(client=user,status__in=allowed_statuses).select_related('client').prefetch_related(
            #     Prefetch('workers', queryset=Staff.objects.select_related('user').prefetch_related('services'))
            # )
        elif filter_param == '':
            queryset = Ticket.objects.filter(client=user).prefetch_related('service')

        return queryset
    
# to update
class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreationSerializer
    permission_classes = [OwnerOrAdminPermission]

# to view
class TicketClientDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketClientDetailSerializer
    permission_classes = [OwnerOrAdminPermission]
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     user = request.user
    #     # Mark related notifications as seen

    #     return super().retrieve(request, *args, **kwargs)

class TicketPictureCreateView(generics.CreateAPIView):
    serializer_class = TicketPictureSerializer

    def perform_create(self, serializer):
        # Get the specific ticket based on URL parameter (e.g., /api/tickets/1/pictures/)
        ticket_id = self.kwargs['pk']
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket_picture = serializer.save()
        ticket_picture.ticket = ticket
        ticket_picture.save()

class TicketPictureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TicketPicture.objects.all()
    serializer_class = TicketPictureSerializer
    permission_classes = [TicketPictureOwnerOrAdminPermission]



# update status
    
class ClientRejectView(generics.UpdateAPIView):
    
    serializer_class = TicketStatusSerializer
    permission_classes = [TicketOwnerPermission]
    
    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(client=user)
    
    def update(self, request, *args, **kwargs):
        # ticket_id = self.kwargs['pk']
        ticket = self.get_object()

        # Validate and update the ticket status
        if ticket.client == request.user:
            ticket.status = 'Client Rejected'
            ticket.save()
            return Response({'message': 'Ticket Rejected successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        
class ClientAcceptView(generics.UpdateAPIView):
    serializer_class = TicketStatusSerializer
    permission_classes = [TicketOwnerPermission]
    
    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(client=user)
    

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()

        if ticket.client == request.user:
            ticket.paycode = generate_payment_code()
            ticket.status = 'Pending Payment'
            ticket.save()
            return Response({'message': 'Ticket Accepted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        

        
class ClientRateView(generics.UpdateAPIView):
    serializer_class = TicketStatusSerializer
    permission_classes = [TicketOwnerPermission]

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(client=user)
    

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        
        rating = request.data.get('client_rating')
        
        if rating is not None and 1 <= rating <= 5:
            if ticket.client == request.user:
                ticket.status = 'Rated'
                ticket.client_rating = rating
                ticket.save()
                return Response({'message': 'Ticket rated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid rating. Please provide a value between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

class StaffRejectTicketView(generics.UpdateAPIView):
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.filter(service__in=user.staff.services.all())
        else:
            return Ticket.objects.none()
        
    
    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        
        if request.user.is_staff:
            staff = request.user.staff
            ticket.assigned_to = staff
            ticket.status = 'Rejected'
            ticket.save()
            return Response({'message': 'Ticket Rejected successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)

class MarkAsPaidView(generics.UpdateAPIView):
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.filter(service__in=user.staff.services.all())
        else:
            return Ticket.objects.none()
        
    
    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        sent_paycode = request.data.get('paycode')
        if request.user.is_staff and ticket.assigned_to == request.user.staff and sent_paycode == ticket.paycode:
            ticket.status = 'In Progress'
            ticket.save()
            return Response({'message': 'Ticket marked as paid successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)

class MarkAsClosedView(generics.UpdateAPIView):
    serializer_class = TicketClosingSerializer
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.filter(service__in=user.staff.services.all())
        else:
            return Ticket.objects.none()
        
    
    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        
        if request.user.is_staff and ticket.assigned_to == request.user.staff :
            if ticket.status != 'In Progress':
                return Response({"message":"Closing the ticket can only be done after the ticket is in progress."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            ticket.status = 'Closed'
            ticket.save()
            return Response({'message': 'Ticket marked as closed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)
class StaffAvailableTicketsList(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [IsAdminUser]

    @method_decorator(cache_page(60*1))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            services = user.staff.services.only('id')
            return Ticket.objects.filter(assigned_to__isnull=True,service__in=services).exclude(status='Rejected').select_related('client').prefetch_related('service')
                    
        else:
            return Ticket.objects.none()


class StaffAssignedTicketsList(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [IsAdminUser]


    @method_decorator(cache_page(60*1))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        status_param = self.request.query_params.get('isfiltered','')
        status_filt = ['Pending Approval','Pending Payment','In Progress']
        if user.is_staff and status_param == 'true':

            return Ticket.objects.filter(assigned_to=user.staff,status__in=status_filt).select_related('client').prefetch_related('service')
        elif user.is_staff and status_param == '':
            return Ticket.objects.filter(assigned_to=user.staff).select_related('client').prefetch_related('service')
        else:
            return Ticket.objects.none()
        

class StaffTicketDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaffTicketDetailsSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.filter(service__in=user.staff.services.all())
        else:
            return Ticket.objects.none()
        
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     user = request.user
    #     # Mark related notifications as see
    #     Notification.objects.filter(ticket=instance,user=user,is_seen=False).update(is_seen=True)
    #     print('Notifications altered')
    #     # for notification in related_notifications:
    #         # notification.is_seen = True
    #         # notification.save()

    #     return super().retrieve(request, *args, **kwargs)

class StaffAssignTicket(generics.RetrieveUpdateAPIView):
    serializer_class = StaffTicketStatusSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.filter(service__in=user.staff.services.all()).select_related('assigned_to','service')
        else:
            return Ticket.objects.none()
    
    def perform_update(self, serializer):
        ticket = serializer.save()
        user = self.request.user
        try:
            staff = Staff.objects.get(user=user)
        except:
            raise Staff.DoesNotExist
        

        # Check if the ticket service is in the staff services
        if ticket.service not in staff.services.all():
            return Response({"detail": "Not allowed. The Ticket Service is not in staff services."},
                            status=status.HTTP_403_FORBIDDEN)
        if ticket.assigned_to != staff:
            ticket.assigned_to = staff
        if not ticket.service.is_final_price:
            ticket.status = 'Pending Approval'
        else:
            ticket.paycode = generate_payment_code()
            ticket.status = 'Pending Payment'

        
        if staff.is_supervisor:
            workers_data = self.request.data.get('workers', None)
            if workers_data is not None:
                workers = []
                for worker_id in workers_data.split(','):
                    try:
                        worker = Staff.objects.get(pk=worker_id,is_supervisor=False)
                        workers.append(worker)
                    except Staff.DoesNotExist:
                        pass
                ticket.workers.set(workers)
        ticket.save()

class WorkerTicketsList(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [IsAdminUser]

    @method_decorator(cache_page(60*1))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.filter(workers=user.staff,status='In Progress').select_related('client').prefetch_related('service')
        else:
            return Ticket.objects.none()
