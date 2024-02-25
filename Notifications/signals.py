from django.db.models.signals import post_save,pre_save, post_delete
from django.dispatch import receiver
from .models import Notification
from Ticket.models import Ticket
from pyfcm import FCMNotification
from django.db import transaction
from django.conf import settings


push_service = FCMNotification(api_key=settings.FCM_API_KEY)

@receiver(post_save,sender=Ticket)
def new_ticket(sender, instance,created, **kwargs):
    if created:
        
        supervisors = instance.service.staffs.filter(is_supervisor=True)

        try:
            with transaction.atomic():
                # Create a notification for each supervisor
                for supervisor in supervisors:
                    
                     # Send the notification to the user's device
                    registration_id = supervisor.user.device_reg_id
                    if registration_id:
                        noti = Notification.objects.create(
                        ticket=instance,
                        user=supervisor.user,
                        type=1
                    )
                        title, body = noti.get_title_body()
                        data_msg={'ticket_id':instance.id,'type':noti.type}
                        push_service.notify_single_device(
                            registration_id=registration_id,
                            message_title=title,
                            message_body=body,
                            data_message=data_msg
                        )
        except Exception as e:
        # Handle any exceptions (e.g., database errors)
        # You can log the error or raise a custom exception
            raise e

@receiver(pre_save,sender=Ticket)
def staff_assign_ticket(sender, instance, **kwargs):
    old_ticket = Ticket.objects.get(pk=instance.pk)
    if old_ticket.assigned_to is None and instance.assigned_to is not None:
        if instance.client.device_reg_id:
            client_noti = Notification.objects.create(user=instance.client,ticket=instance,type=2)
            title, body = client_noti.get_title_body()
            data_msg={'ticket_id':instance.id,'type':client_noti.type}
            push_service.notify_single_device(
                registration_id=instance.client.device_reg_id,
                message_title=title,
                message_body=body,
                data_message=data_msg
            )

@receiver(pre_save,sender=Ticket)
def staff_reject_ticket(sender, instance, **kwargs):
    old_ticket = Ticket.objects.get(pk=instance.pk)
    if old_ticket.status =='Open' and instance.status == 'Rejected':
        if instance.client.device_reg_id:
            client_noti = Notification.objects.create(user=instance.client,ticket=instance,type=6)
            title, body = client_noti.get_title_body()
            data_msg={'ticket_id':instance.id,'type':client_noti.type}
            push_service.notify_single_device(
                registration_id=instance.client.device_reg_id,
                message_title=title,
                message_body=body,
                data_message=data_msg
            )
    
@receiver(pre_save,sender=Ticket)
def client_reject_ticket(sender, instance, **kwargs):
    old_ticket = Ticket.objects.get(pk=instance.pk)
    if old_ticket.status == 'Pending Approval' and instance.status == 'Client Rejected':
        if instance.assigned_to.user.device_reg_id:
            staff_noti = Notification.objects.create(user=instance.assigned_to.user,ticket=instance,type=3)
            title, body = staff_noti.get_title_body()
            data_msg={'ticket_id':instance.id,'type':staff_noti.type}
            push_service.notify_single_device(
                registration_id=instance.assigned_to.user.device_reg_id,
                message_title=title,
                message_body=body,
                data_message=data_msg
            )


@receiver(pre_save,sender=Ticket)
def client_accept_ticket(sender, instance, **kwargs):
    old_ticket = Ticket.objects.get(pk=instance.pk)
    if old_ticket.status == 'Pending Approval' and instance.status == 'Pending Payment':
        if instance.assigned_to.user.device_reg_id:
            staff_noti = Notification.objects.create(user=instance.assigned_to.user,ticket=instance,type=4)
            title, body = staff_noti.get_title_body()
            data_msg={'ticket_id':instance.id,'type':staff_noti.type}
            push_service.notify_single_device(
                registration_id=instance.assigned_to.user.device_reg_id,
                message_title=title,
                message_body=body,
                data_message=data_msg
            )

@receiver(pre_save,sender=Ticket)
def ticket_paid(sender, instance, **kwargs):
    old_ticket = Ticket.objects.get(pk=instance.pk)
    if old_ticket.status == 'Pending Payment' and instance.status == 'In Progress':
        if instance.client.device_reg_id:
            client_noti = Notification.objects.create(user=instance.client,ticket=instance,type=5)
            title, body = client_noti.get_title_body()
            data_msg={'ticket_id':instance.id,'type':client_noti.type}
            push_service.notify_single_device(
                registration_id=instance.assigned_to.user.device_reg_id,
                message_title=title,
                message_body=body,
                data_message=data_msg
            )
        workers = instance.workers.all()
        for worker in workers:
                    
                     # Send the notification to the user's device
                    registration_id = worker.user.device_reg_id
                    if registration_id:
                        noti = Notification.objects.create(
                        ticket=instance,
                        user=worker.user,
                        type=5
                    )
                        title = 'Ticket in progress'
                        body = 'There is a Ticket paid and must be work on'
                        data_msg={'ticket_id':instance.id,'type':noti.type}
                        push_service.notify_single_device(
                            registration_id=registration_id,
                            message_title=title,
                            message_body=body,
                            data_message=data_msg
                        )