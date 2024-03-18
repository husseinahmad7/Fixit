from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
# from Users.models import Staff, User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
# from django.core.files.storage import default_storage
# Create your models here.
# import uuid

from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()


class ServiceCategory(models.Model):
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='cat_icons/', storage=gd_storage)
    def __str__(self):
        return self.title

class Service(models.Model):
    TYPES = [
        ('Fixing', 'Fixing service'),
        ('Support', 'Support service'),
        ('Setting', 'Setting service')
        
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    picture = models.ImageField(upload_to='serv_pictures/',storage=gd_storage)
    type = models.CharField(max_length=10,choices=TYPES,default='Fixing')
    is_final_price = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Rejected', 'Rejected by company'),
        ('Pending Approval', 'Pending for client approval'),
        ('Client Rejected', 'Rejected by client'),
        ('Pending Payment', 'Pending for client payment'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
        ('Rated', 'Rated'),

    ]
    
    client = models.ForeignKey('Users.User', on_delete=models.CASCADE,db_index=True)
    # title = models.CharField(max_length=200)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    location = models.JSONField()
    info_fields = models.JSONField(null=True, blank=True)
    assigned_to = models.ForeignKey('Users.Staff', on_delete=models.CASCADE, related_name='tickets', null=True, blank=True,db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Open',db_index=True)
    client_rating = models.IntegerField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    submission_date = models.DateTimeField(auto_now_add=True,db_index=True)
    workers = models.ManyToManyField('Users.Staff', related_name='tickets_assigned', blank=True,limit_choices_to={'is_supervisor': False})
    paycode = models.CharField(max_length=20,blank=True,null=True)

    class Meta:
        ordering = ['submission_date']
    def __str__(self) -> str:
        return f'{self.pk} -- {self.status}'


class TicketPicture(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to='attachments/',storage=gd_storage)

@receiver(post_delete, sender=TicketPicture)
def delete_ticket_picture(sender, instance, **kwargs):
    if instance.picture:
        instance.picture.delete(save=False)

@receiver(post_delete, sender=ServiceCategory)
def delete_cat_icon(sender, instance, **kwargs):
    if instance.icon:
        instance.icon.delete(save=False)

@receiver(post_delete, sender=Service)
def delete_service_picture(sender, instance, **kwargs):
    if instance.picture:
        instance.picture.delete(save=False)

@receiver(pre_save, sender=ServiceCategory)
def delete_old_cat_picture(sender, instance, **kwargs):
    if instance.pk:
        old_cat = ServiceCategory.objects.get(pk=instance.pk)
        if old_cat.icon != instance.icon:
            old_cat.icon.delete(save=False)
            

@receiver(pre_save, sender=Service)
def delete_old_service_picture(sender, instance, **kwargs):
    if instance.pk:
        old_service = Service.objects.get(pk=instance.pk)
        if old_service.picture != instance.picture:
            old_service.picture.delete(save=False)
            

@receiver(pre_save, sender=TicketPicture)
def delete_old_ticket_picture(sender, instance, **kwargs):
    if instance.pk:
        old_ticketpic = TicketPicture.objects.get(pk=instance.pk)
        if old_ticketpic.picture != instance.picture:
            old_ticketpic.picture.delete(save=False)
