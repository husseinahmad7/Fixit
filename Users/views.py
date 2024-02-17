# from django.shortcuts import render
# from .models import User
from django.utils.decorators import method_decorator

# from django.views.generic import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer,StaffSerializer ,WorkerSerializer ,UserRegistrationSerializer, PasswordChangeSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser, AllowAny
from rest_framework import status
from .permissins import IsSuperUser, IsUserOrReadOnly
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.debug import sensitive_post_parameters
sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Staff
from django.core.cache import cache
import random
from Ticket.models import Service

def generate_6_digit_code():
    return random.randint(100000, 999999)

class UsersListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    serializer_class = UserSerializer
    queryset = User.objects.all()
    
class UsersRetrieveDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    
class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # queryset = User.objects.all()
    permission_classes = [IsUserOrReadOnly]

class StaffListApiView(generics.ListAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()

class StaffsRetrieveDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    # def perform_update(self, serializer):
    #     services_data = self.request.data.get('services')
    #     staff = Staff.objects.get(pk=self.request.kwargs['pk'])
    #     if services_data is not None:
    #         # staff.services.clear()
    #         # for service_data in services_data:
    #         #     service = Service.objects.get(pk=service_data['id'])
    #         #     staff.services.add(service)
    #         # staff.save()

            
    #         staff = Staff.objects.update(department=self.request.data.get('department'),salary=self.request.data.get('salary'),availability=self.request.data.get('availability'),is_supervisor=self.request.data.get('is_supervisor'))
    #         services = self.request.data.get('services').split(',')
    #         list = []
    #         for serv in services:
    #             service = Service.objects.get(pk=serv)
    #             list.append(service)
    #         staff.services.set(list)

class ServiceWorkersList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = WorkerSerializer
    
    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        service = Service.objects.get(pk=service_id)
        return Staff.objects.filter(services=service,is_supervisor=False)

class AddServiceForStaffView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request, pk):
        try:
            staff = Staff.objects.get(id=pk)
        except Staff.DoesNotExist:
            return Response({'message': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)

        service_id = request.data.get('service_id')
        if not service_id:
            return Response({'message': 'Service id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        service = Service.objects.get(pk=service_id)
        if service in staff.services.all():
            return Response({'message': 'Service already exists.'}, status=status.HTTP_200_OK)
        else:

            staff.services.add(service)
            return Response({'message': f'Service {service.title} addded successfully for {staff.user.full_name}.'}, status=status.HTTP_200_OK)
            


class DeleteServiceForStaffView(APIView):
    def delete(self, request, pk, srv_pk):
        try:
            staff = Staff.objects.get(id=pk)
        except Staff.DoesNotExist:
            return Response({'message': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            service = Service.objects.get(pk=srv_pk)
        except Service.DoesNotExist:
            return Response({'message': 'Service not found.'}, status=status.HTTP_404_NOT_FOUND)

        staff.services.remove(service)
        return Response({'message': f'Service {service.title} removed from staff {staff.user.full_name} successfully.'}, status=status.HTTP_200_OK)
    

# class RegistrationView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
            
#             user = serializer.save()
#             password = request.data.get('password')
#             user.set_password(password)
#             user.save()
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'Token': token.key}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserRegistrationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            client.is_active = False
            client.save()
            code = generate_6_digit_code()
            
            cache.set(f'confirmation_code_{client.id}', code)
            send_mail(
                'Activate your account',
                f'Please copy the code below to activate your account:\n{code}',
                'noreply@Fixit.com',
                [client.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ActivateUserAPIView(APIView):
    def post(self, request):
        try:
            # uid = force_str(urlsafe_base64_decode(request.data.get('code1')))
            email = request.data.get('email')
            user = get_user_model().objects.get(email=email)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        code = request.data.get('code')

        cache_code =cache.get(f'confirmation_code_{user.id}')

        if int(code) == int(cache_code):
            user.is_active = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            data = {
                    'token': token.key,
                    'id': user.id,
                    
                    'email': user.email,
                    'full_name':user.full_name,
                    'is_staff': user.is_staff,
                    'mobile': user.mobile
                }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation Code is invalid!'}, status=status.HTTP_400_BAD_REQUEST)


class StaffRegistrationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            password = request.data.get('password')
            user.set_password(password)
            user.is_staff = True
            user.save()
            
            staff = Staff.objects.create(user=user,department=request.data.get('department'),salary=request.data.get('salary'),availability=request.data.get('availability'),is_supervisor=request.data.get('is_supervisor'))
            services = self.request.data.get('services').split(',')
            list = []
            for serv in services:
                service = Service.objects.get(pk=serv)
                list.append(service)
            staff.services.set(list)
            # token, created = Token.objects.get_or_create(user=user)
            return Response({'success': 'Stuff user Created Successfully','pk':staff.pk}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"message":"Already logged in."})
        return Response({""})
    def post(self, request):
        # Get the email and password from the request body
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request=request, email=email, password=password)
        if user is not None:
            if user.is_active:
                # Generate a token for the user
                token,created = Token.objects.get_or_create(user=user)
                data = {
                    'token': token.key,
                    'id': user.id,
                    
                    'email': user.email,
                    'full_name':user.full_name,
                    'is_staff': user.is_staff,
                    'mobile': user.mobile
                }
                 # Include additional staff information if the user is a staff member
                if user.is_staff:
                    staff_info = {
                        'staff_id': user.staff.id,
                        'is_supervisor': user.staff.is_supervisor,
                        'department':user.staff.department,
                        'salary': user.staff.salary,
                        'availability': user.staff.availability,
                        'services': user.staff.services
                    }
                    data.update(staff_info)
                # Return the token in the response body
                return Response(data,status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Please activate your acount first'},status=status.HTTP_403_FORBIDDEN)

        else:
            # Return an error response
            return Response({'error': 'Invalid credentials'}, status=400)
    
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Get the user's token

        token = self.request.user.auth_token
        # Check if the token exists
        if token is not None:
            # Delete the user's token
            token.delete()
        

        # Return a success response
        return Response({'success': 'User logged out successfully.'})




class AdminView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = authenticate(request=request, token=request.auth)
        if user.is_superuser:
            # Return the admin view
            pass
        else:
            # Return the non-admin view
            pass


class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    # @sensitive_post_parameters_m
    # def dispatch(self, *args, **kwargs):
    #     return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )


class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})
