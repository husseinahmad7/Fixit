# from pyfcm import FCMNotification
# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter notifications for the current user
        return self.queryset.filter(user=self.request.user)

class MarkNotificationAsSeenView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        # Mark the notification as seen
        instance = self.get_object()
        instance.is_seen = True
        instance.save()
        return self.partial_update(request, *args, **kwargs)


class UnseenNotificationCountView(APIView):
    def get(self, request):
        # Retrieve the current user's unseen notifications
        unseen_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        return Response({'unseen_count': unseen_count})