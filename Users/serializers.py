from rest_framework import serializers
# from .models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.conf import settings
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.contrib.auth.tokens import default_token_generator
from .models import Staff
from Ticket.models import Service
from Ticket.serializers import ServiceSerializer
from django.core.validators import RegexValidator
# Get the UserModel
UserModel = get_user_model()
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'full_name','is_staff', 'mobile']
        
class StaffSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=True))
    
    email = serializers.SerializerMethodField()
    services = serializers.ManyRelatedField(child_relation=ServiceSerializer())
    # is_staff = serializers.HiddenField(readonly=True,default=True)
    class Meta:
        model = Staff
        fields = ['id', 'user','email', 'department', 'salary', 'availability', 'services','is_supervisor']
    def get_email(self, obj):
        return obj.user.email
    
    def update(self, instance, validated_data):
        services_data = validated_data.pop('services', None)
        if services_data is not None:
            services = []
            for service_id in services_data.split(','):
                try:
                    service = Service.objects.get(pk=service_id)
                    services.append(service)
                except Service.DoesNotExist:
                    pass
            instance.services.set(services)
        return instance

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'user', 'department', 'salary', 'availability', 'services']
# class StaffCSerializer(serializers.ModelSerializer):
#     # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     email = serializers.EmailField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     department = serializers.CharField()
#     salary = serializers.DecimalField(max_digits=10, decimal_places=2,default=0.)
#     availability = serializers.BooleanField(default=True)
#     is_supervisor = serializers.BooleanField(default=True)
#     mobile = serializers.IntegerField()
#     services = serializers.ManyRelatedField(child_relation=ServiceSerializer)
#     # is_staff = serializers.HiddenField(readonly=True,default=True)
#     class Meta:
#         model = Staff
#         fields = ['username','email','password','first_name','last_name','mobile', 'department', 'salary', 'availability','is_supervisor', 'services']
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    mobile_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Mobile number must be exactly 10 digits."
    )

    mobile = serializers.CharField(validators=[mobile_regex])
    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password','full_name', 'mobile']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            mobile=validated_data['mobile'],
            full_name=validated_data['full_name'],
            
        )
        user.set_password(validated_data['password']) 
        user.is_active = False
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'subject_template_name':"Users/password_reset_subject.txt",
            "email_template_name": 'Users/reset-pass-email.html',
            
            
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)
