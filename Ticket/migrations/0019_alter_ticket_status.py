# Generated by Django 5.0.1 on 2024-03-16 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0018_ticket_paycode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Rejected', 'Rejected by company'), ('Pending Approval', 'Pending for client approval'), ('Client Rejected', 'Rejected by client'), ('Pending Payment', 'Pending for client payment'), ('In Progress', 'In Progress'), ('Closed', 'Closed'), ('Rated', 'Rated')], db_index=True, default='Open', max_length=20),
        ),
    ]