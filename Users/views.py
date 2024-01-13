# from django.shortcuts import render
# from .models import User
from django.utils.decorators import method_decorator

# from django.views.generic import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer,StaffSerializer ,UserRegistrationSerializer, PasswordChangeSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
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
from .models import Staff, Skill
from django.core.cache import cache
import random

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
    queryset = User.objects.all()
    permission_classes = [IsUserOrReadOnly]

class StaffListApiView(generics.ListAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()


class StaffsRetrieveDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    serializer_class = StaffSerializer
    queryset = Staff.objects.all()

class AddSkillForStaffView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def post(self, request, pk):
        try:
            staff = Staff.objects.get(id=pk)
        except Staff.DoesNotExist:
            return Response({'message': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)

        skill_name = request.data.get('name')
        if not skill_name:
            return Response({'message': 'Skill name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        skill, created = Skill.objects.get_or_create(name=skill_name)
        if created:
            staff.skills.add(skill)
            return Response({'message': f'Skill {skill.name} created successfully for {staff.user.username}.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Skill already exists.'}, status=status.HTTP_200_OK)


class DeleteSkillForStaffView(APIView):
    def delete(self, request, pk, skill_name):
        try:
            staff = Staff.objects.get(id=pk)
        except Staff.DoesNotExist:
            return Response({'message': 'Staff not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            skill = Skill.objects.get(name=skill_name)
        except Skill.DoesNotExist:
            return Response({'message': 'Skill not found.'}, status=status.HTTP_404_NOT_FOUND)

        staff.skills.remove(skill)
        return Response({'message': f'Skill {skill.name} removed from staff {staff.user.username} successfully.'}, status=status.HTTP_200_OK)
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
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            client.is_active = False
            client.save()
            # uidb64 = urlsafe_base64_encode(force_bytes(client.pk))
            # token = default_token_generator.make_token(client)
            code = generate_6_digit_code() # Replace this with your own code to generate a 6-digit code
            print(code)
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
            return Response({'token': token.key}, status=status.HTTP_200_OK)
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
            staff = Staff.objects.create(user=user,salary=request.data.get('salary'))
            # token, created = Token.objects.get_or_create(user=user)
            return Response({'success': 'Stuff user Created Successfully','pk':staff.pk}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def get(self, request):
        if request.user.is_authenticated():
            return Response({""})
        return Response({""})
    def post(self, request):
        # Get the username and password from the request body
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            # Generate a token for the user
            token = Token.objects.create(user=user)

            # Return the token in the response body
            return Response({'token': token.key})
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
