from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
# from Ticket.models import Service


from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField("Email address", unique=True)
    full_name = models.CharField("Full name",max_length=30)
    mobile = models.CharField("Mobile",max_length=20,blank=True,null=True)
    device_reg_id = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'mobile']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse("user-info", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"{self.full_name}"


class Staff(models.Model):
    
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2,default=0.)
    availability = models.BooleanField(default= True)
    services = models.ManyToManyField('Ticket.Service',related_name='staffs', blank=True)
    is_supervisor = models.BooleanField(default= False)

    def get_absolute_url(self):
        return reverse("staff-retrieve", kwargs={"pk": self.pk})
    def __str__(self):
        return f"{self.user.full_name}"
    
    class Meta:
        ordering = ['department']