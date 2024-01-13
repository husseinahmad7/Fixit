from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from Users.models import Staff
# Create your models here.
# import uuid
class ServiceCategory(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.title
    


class Ticket(models.Model):
    # unique_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # category = models.CharField(max_length=100)
    # maintenance_help = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    discription = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    approved = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    status = models.CharField(max_length=100)
    client_rating = models.IntegerField()
    notes = models.TextField()
    is_paid = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    # qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    workers = models.ManyToManyField(Staff, related_name='tickets_assigned', blank=True)

    class Meta:
        ordering = ['submission_date']
    # def clean(self):
    #     if self.assigned_to_staff and not self.assigned_to_staff.is_supervisor:
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