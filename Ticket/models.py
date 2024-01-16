from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
# from Users.models import Staff, User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
# Create your models here.
# import uuid
class ServiceCategory(models.Model):
    title = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='cat_icons/')
    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    picture = models.ImageField(upload_to='serv_pictures/')

    def __str__(self):
        return self.title
    


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    ]
    client = models.ForeignKey('Users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    approved = models.BooleanField(default=False)
    assigned_to = models.ForeignKey('Users.Staff', on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,default='Open')
    client_rating = models.IntegerField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    is_paid = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    # qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    workers = models.ManyToManyField('Users.Staff', related_name='tickets_assigned', blank=True)

    class Meta:
        ordering = ['submission_date']
    def __str__(self) -> str:
        return f'{self.pk} {self.title} -- {self.status}'
    # def clean(self):
    #     if self.assigned_to and not self.assigned_to.is_supervisor:
    #         raise ValidationError({"detail": "Assigned staff member must be a supervisor"})
    
    # def save(self, *args, **kwargs):
    #     # Generate QR code
    #     qr = qrcode.QRCode(version=1, box_size=10, border=5)
    #     qr.add_data(str(self.pk))
    #     qr.make(fit=True)
    #     img = qr.make_image(fill_color='black', back_color='white')

    #     # Save QR code image to buffer
    #     buffer = BytesIO()
    #     img.save(buffer, 'PNG')
    #     self.qr_code.save(f'{self.pk}.png', File(buffer), save=False)
    #     buffer.close()
        
    #     super().save(*args, **kwargs)


class TicketPicture(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to='attachments/')

@receiver(post_delete, sender=TicketPicture)
def delete_ticket_picture(sender, instance, **kwargs):
    if instance.picture:
        default_storage.delete(instance.picture.name)

@receiver(post_delete, sender=ServiceCategory)
def delete_cat_icon(sender, instance, **kwargs):
    if instance.icon:
        default_storage.delete(instance.icon.name)

@receiver(post_delete, sender=Service)
def delete_service_picture(sender, instance, **kwargs):
    if instance.picture:
        default_storage.delete(instance.picture.name)

@receiver(pre_save, sender=ServiceCategory)
def delete_old_cat_picture(sender, instance, **kwargs):
    if instance.pk:
        old_cat = ServiceCategory.objects.get(pk=instance.pk)
        if old_cat.icon != instance.icon:
            default_storage.delete(old_cat.icon.name)

@receiver(pre_save, sender=Service)
def delete_old_service_picture(sender, instance, **kwargs):
    if instance.pk:
        old_service = Service.objects.get(pk=instance.pk)
        if old_service.picture != instance.picture:
            default_storage.delete(old_service.picture.name)

@receiver(pre_save, sender=TicketPicture)
def delete_old_ticket_picture(sender, instance, **kwargs):
    if instance.pk:
        old_ticketpic = TicketPicture.objects.get(pk=instance.pk)
        if old_ticketpic.picture != instance.picture:
            default_storage.delete(old_ticketpic.picture.name)