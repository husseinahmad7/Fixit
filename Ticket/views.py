from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket

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
