from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from Users.permissins import IsSuperUser
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import Ticket, Service, ServiceCategory, TicketPicture
from .serializers import TicketSerializer, ServiceSerializer, ServiceCategorySerializer, TicketCreationSerializer,TicketPictureSerializer,TicketStatusSerializer, StaffTicketSerializer
from Users.models import Staff
# from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import OwnerOrAdminPermission,TicketPictureOwnerOrAdminPermission
# reading categories
class ServiceCategoryList(generics.ListAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    def get_queryset(self):
        # Assuming you have a category ID passed as a query parameter (e.g., ?category_id=1)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            return Service.objects.filter(service_category__id=category_id)
        else:
            # Return all services if no category ID is provided
            return Service.objects.all()
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
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.filter(client=user)
        # Check if the 'filtered' parameter is set to 'true'
        filter_param = self.request.query_params.get('filtered')
        if filter_param == 'true':
            # Customize the status values as needed 
            allowed_statuses = ['Open', 'In Progress', 'Pending','Closed']

            # Filter tickets based on the allowed statuses
            queryset = queryset.filter(status__in=allowed_statuses)

        return queryset
    

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreationSerializer
    permission_classes = [OwnerOrAdminPermission]

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
    # queryset = Ticket.objects.all()
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # ticket_id = self.kwargs['pk']
        ticket = self.get_object()

        # Validate and update the ticket status
        if ticket.client == request.user:
            ticket.status = 'Client Rejected'
            ticket.save()
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        
class ClientAcceptView(generics.UpdateAPIView):
    # queryset = Ticket.objects.all()
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()

        if ticket.client == request.user:
            ticket.status = 'Pending Payment'
            ticket.save()
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        

        
class ClientRateView(generics.UpdateAPIView):
    # queryset = Ticket.objects.all()
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        rating = request.data.get('client_rating')
        if ticket.client == request.user:
            ticket.client_rating = rating
            ticket.save()
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)

class MarkAsPaidView(generics.UpdateAPIView):
    serializer_class = TicketStatusSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        
        if request.user.is_staff:
            ticket.status = 'In Progress'
            ticket.save()
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({'error': 'Action is not allowed.'}, status=status.HTTP_403_FORBIDDEN)

class StaffTicketsList(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.filter(service__in=user.staff.services.all())
        else:
            return Ticket.objects.none()


class StaffAssignTicket(generics.RetrieveUpdateAPIView):
    serializer_class = StaffTicketSerializer
    permission_classes = [IsAdminUser]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return Ticket.objects.filter(service__in=user.staff.services.all())
    #     else:
    #         return Ticket.objects.none()
    
    def perform_update(self, serializer):
        ticket = serializer.save()
        user = self.request.user
        try:
            staff = Staff.objects.get(user=user)
        except:
            raise Staff.DoesNotExist
        if ticket.assigned_to != staff:
            ticket.assigned_to = staff

        # Check if the ticket service is in the staff services
        if ticket.service not in staff.services.all():
            return Response({"detail": "Not allowed. The Ticket Service is not in staff services."},
                            status=status.HTTP_403_FORBIDDEN)
        
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
# class QRCodeScanView(APIView):
#     def post(self, request):
#         qr_code_path = request.data.get('qr_code')
#         staff_id = request.data.get('staff_id')

#         try:
#             ticket = Ticket.objects.get(qr_code=qr_code_path, assigned_to_staff_id=staff_id)
#         except Ticket.DoesNotExist:
#             return Response({'message': 'Invalid QR code or staff ID'}, status=status.HTTP_400_BAD_REQUEST)

#         ticket.is_paid = True
#         ticket.status = 'Done'
#         ticket.save()

#         return Response({'message': 'Ticket marked as paid and done'}, status=status.HTTP_200_OK)

