from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from Users.permissins import IsSuperUser

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .models import Ticket, Service, ServiceCategory
from .serializers import TicketSerializer, ServiceSerializer, ServiceCategorySerializer, TicketCreationSerializer

# reading categories
class ServiceCategoryList(generics.ListAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ServiceCategoryCreate(generics.CreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsSuperUser]

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

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsSuperUser]

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

    # def perform_update(self, serializer):
    #     ticket = serializer.save()
    #     if ticket.status == 'Closed':
    #         ticket.client_rating = self.request.data.get('client_rating')
    #         ticket.save()


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
