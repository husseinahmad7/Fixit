from django.urls import path
from .views import ServiceCategoryList,ServiceCategoryCreate,ServiceCategoryDetail,ServiceList,ServiceCreate,ServiceDetail,TicketCreate,ClientTicketsList,TicketDetail
urlpatterns = [
    path('service/cat/list',ServiceCategoryList.as_view()),
    path('service/cat/create',ServiceCategoryCreate.as_view()),
    path('service/cat/<int:pk>',ServiceCategoryDetail.as_view()),
    path('service/list',ServiceList.as_view()),
    path('service/create',ServiceCreate.as_view()),
    path('service/<int:pk>',ServiceDetail.as_view()),
    path('create/',TicketCreate.as_view()),
    path('list/',ClientTicketsList.as_view()),
    path('client_update/<int:pk>/',TicketDetail.as_view()),


]