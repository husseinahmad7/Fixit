# from pyfcm import FCMNotification
# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer,NotificationSeenActSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Ticket.decorators import query_debugger
from django.utils.decorators import method_decorator

@method_decorator(query_debugger,name='dispatch')
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter notifications for the current user
        user = self.request.user
        filtered = self.request.query_params.get('filtered', None)

        if filtered == 'true':
            # Retrieve unseen notifications (where 'unseen' is True)
            unseen_notifications = Notification.objects.filter(user=user, is_seen=False).select_related('ticket__client')
            return unseen_notifications
        else:
            # Show all notifications
            return Notification.objects.filter(user=user).select_related('ticket__client')
        # return self.queryset.filter(user=self.request.user)

class MarkNotificationAsSeenView(generics.UpdateAPIView):
    queryset = Notification.objects.all().select_related('ticket')
    serializer_class = NotificationSeenActSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        # Mark the notification as seen
        user = request.user
        instance = self.get_object()
        # instance.is_seen = True
        # instance.save()
        Notification.objects.filter(ticket=instance.ticket,user=user,is_seen=False).update(is_seen=True)

        return Response({'success': 'The Notification has been seen.'},status=status.HTTP_200_OK)
        


class UnseenNotificationCountView(APIView):
    def get(self, request):
        # Retrieve the current user's unseen notifications
        unseen_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        return Response({'unseen_count': unseen_count})