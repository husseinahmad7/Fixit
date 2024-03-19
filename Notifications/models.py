from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPE = ((1,'new ticket'),(2,'staff assign ticket'), (3,'client reject'),
                          (4,'client accept'),(5,'paid ticket'),(6,'ticket rejected'),(7,'ticket done'),(8,'ticket rated'))
    
    ticket = models.ForeignKey('Ticket.Ticket',on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE,db_index=True)
    type = models.IntegerField(choices=NOTIFICATION_TYPE)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False,db_index=True)
    class Meta:
        ordering = ['-date']

    def get_title_body(self):
        match self.type:
            case 1:
                return ('Ticket available',f'A new ticket is available')
            case 2:
                if self.ticket.final_price is not None:

                    return ('Ticket got priced',f'Your Ticket is pending to approve the final price {self.ticket.final_price}')
                else:
                    return ('Ticket Assigned','Your have to be pay your ticket now')
            case 3:
                return ('Ticket rejected',f'The Ticket has been rejected by {self.ticket.client.full_name}')

            case 4:
                return ('Ticket accepted',f'The Ticket has been accepted by {self.ticket.client.full_name}')

            case 5:
                return ('Ticket paid',f'The Ticket has been paid and ready to work on')
            case 6:
                return ('Ticket rejected',f'The Ticket has been rejected')
            case 7:
                return ('Ticket done', 'You can rate the Ticket service now')
            case 8:
                return ('Ticket rated',f'A ticket has been rated {self.ticket.client_rating}')
            case _:
                return (f'',f'')