from django.shortcuts import render

# Create your views here.
# from pyfcm import FCMNotification
# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

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
