from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User

class User(AbstractUser):
    mobile = models.CharField("mobile",max_length=20,blank=True,null=True)
    email = models.EmailField("email address", unique=True)
    
    def get_absolute_url(self):
        return reverse("user-info", kwargs={"pk": self.pk})

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.name}"

# class Client(models.Model):
#     user = models.OneToOneField('User', on_delete=models.CASCADE)
#     address = models.CharField(max_length=200)

class Staff(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2,default=0.)
    availability = models.BooleanField(default= True)
    skills = models.ManyToManyField(Skill, blank=True)
    is_supervisor = models.BooleanField(default= False)

    def get_absolute_url(self):
        return reverse("staff-retrieve", kwargs={"pk": self.pk})
    
# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(username, email, password, **extra_fields)


# class Client(AbstractBaseUser, PermissionsMixin):
#     contact = models.CharField(max)
    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name='groups',
    #     blank=True,
    #     help_text=
    #         'The groups this user belongs to. A user will get all permissions '
    #         'granted to each of their groups.'
    #     ,
    #     related_name='users',
    #     related_query_name='user',
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     verbose_name='user permissions',
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     related_name='users_permissions',
    #     related_query_name='user_permissions',
    # )
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = []

    # objects = UserManager()

    # def __str__(self):
    #     return f"{self.username}"
