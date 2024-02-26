from django.urls import path
from .views import NotificationListView, MarkNotificationAsSeenView,UnseenNotificationCountView
urlpatterns = [
    path('list/',NotificationListView.as_view()),
    path('seen/<int:pk>/',MarkNotificationAsSeenView.as_view()),
    path('unseen/',UnseenNotificationCountView.as_view()),
]