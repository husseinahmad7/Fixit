from django.urls import path
from .views import LoginView,UsersListCreateView,StaffsRetrieveDeleteUpdateView,StaffListApiView,ServiceWorkersList,UserRegistrationAPIView,ActivateUserAPIView,UserRetrieveUpdateAPIView, UsersRetrieveDeleteUpdateView,LogoutView,StaffRegistrationView,PasswordChangeView,PasswordResetConfirmView,PasswordResetView,AddServiceForStaffView,DeleteServiceForStaffView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [

    # path('register/', RegistrationView.as_view(),name='register'),
    path('register/', UserRegistrationAPIView.as_view(),name='register'),
    path('activate/', ActivateUserAPIView.as_view(),name='register-activate'),
    path('user/<int:pk>/', UserRetrieveUpdateAPIView.as_view(),name='user-info'),
    
    #Login ,obtain the token using username and password
    path('token/', obtain_auth_token, name='token'),
    path('login/', LoginView.as_view(), name='login'),
    # staff stuff
    path('st/', UsersListCreateView.as_view(),name='api'),
    path('st/register/staff', StaffRegistrationView.as_view(),name='register-staff'),
    path('st/user/<int:pk>/', UsersRetrieveDeleteUpdateView.as_view(),name='retrieve'),
    path('st/staff/<int:pk>/', StaffsRetrieveDeleteUpdateView.as_view(),name='staff-retrieve'),
    path('st/stafflist/', StaffListApiView.as_view(),name='staff-list'),
    path('st/workerslistbyserv/<int:service_id>', ServiceWorkersList.as_view(),name='workers-list-byserv'),

    path('st/staff/<int:pk>/addsrv', AddServiceForStaffView.as_view(),name='staff-task-add'),
    path('st/staff/<int:pk>/removesrv/<int:srv_pk>', DeleteServiceForStaffView.as_view(),name='staff-task-add'),

    #path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # password
    path('password/reset/', PasswordResetView.as_view(),
        name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(),
        name='rest_password_change'),
]
