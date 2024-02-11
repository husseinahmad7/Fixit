from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from Users.permissins import IsSuperUser
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import Ticket, Service, ServiceCategory
from .serializers import TicketSerializer, ServiceSerializer, ServiceCategorySerializer, TicketCreationSerializer, StaffTicketSerializer
from Users.models import Staff
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
    serializer_class = TicketCreationSerializer
    permission_classes = [IsAuthenticated]

class ClientTicketsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(client=user)
    

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.filter(service__in=user.staff.services.all())
        else:
            return Ticket.objects.none()
    
    def perform_update(self, serializer):
        ticket = serializer.save()
        user = self.request.user
        try:
            staff = Staff.objects.get(user=user)
        except:
            raise Staff.DoesNotExist
        if ticket.assigned_to != staff:
            ticket.assigned_to = staff

        if staff.is_supervisor:
            workers_data = self.request.data.get('workers', None)
            if workers_data is not None:
                workers = []
                for worker_id in workers_data.split(','):
                    try:
                        worker = Staff.objects.get(pk=worker_id)
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
