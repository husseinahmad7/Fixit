from django.urls import path
from .views import ServiceCategoryList,ServiceCategoryCreate,ServiceCategoryDetail,ServiceList,ServiceListByRating,ServiceCreate,ServiceDetail,ServiceRetrieve,ServiceListByCategory,TicketCreate,ClientTicketsList,TicketDetail,TicketClientDetail,TicketPictureCreateView,TicketPictureDetail,ClientRejectView,ClientAcceptView,StaffRejectTicketView,MarkAsPaidView,MarkAsClosedView,ClientRateView, StaffAvailableTicketsList,StaffAssignedTicketsList, StaffTicketDetailsView,StaffAssignTicket,WorkerTicketsList
urlpatterns = [
    path('service/cat/list',ServiceCategoryList.as_view()),
    path('service/cat/create',ServiceCategoryCreate.as_view()),
    path('service/cat/<int:pk>',ServiceCategoryDetail.as_view()),
    path('service/list',ServiceList.as_view()),
    path('service/listbyrate',ServiceListByRating.as_view()),
    path('service/create',ServiceCreate.as_view()),
    path('service/<int:pk>',ServiceDetail.as_view()),
    path('service/show/<int:pk>',ServiceRetrieve.as_view()),

    path('create/',TicketCreate.as_view()),
    path('list/',ClientTicketsList.as_view()),
    path('client_update/<int:pk>/',TicketDetail.as_view()),
    path('client_view/<int:pk>/',TicketClientDetail.as_view()),
    path('client_update/<int:pk>/add_pic',TicketPictureCreateView.as_view()),
    path('ticketpicture/<int:pk>/',TicketPictureDetail.as_view()),
    path('staff_ticket_details/<int:pk>',StaffTicketDetailsView.as_view()),
    path('staff_assign_update/<int:pk>/',StaffAssignTicket.as_view()),
    path('staff_available_tickets_list/',StaffAvailableTicketsList.as_view()),
    path('staff_assigned_tickets_list/',StaffAssignedTicketsList.as_view()),
    path('workers_tickets_list/',WorkerTicketsList.as_view()),
    path('services_by_category/', ServiceListByCategory.as_view(), name='service-list-by-category'),
    path('action/client_reject/<int:pk>',ClientRejectView.as_view()),
    path('action/client_accept/<int:pk>',ClientAcceptView.as_view()),
    path('action/staff_reject_ticket/<int:pk>',StaffRejectTicketView.as_view()),
    path('action/mark_as_paid/<int:pk>',MarkAsPaidView.as_view()),
    path('action/mark_as_closed/<int:pk>',MarkAsClosedView.as_view()),
    path('action/client_rate/<int:pk>',ClientRateView.as_view()),


]