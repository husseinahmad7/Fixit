# Generated by Django 5.0.1 on 2024-04-18 07:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Ticket', '0001_initial'),
        ('Users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='assigned_to',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_supervisor': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='Users.staff'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='client',
            field=models.ForeignKey(limit_choices_to={'is_staff': False}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='Ticket.service'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='workers',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_supervisor': False}, related_name='tickets_assigned', to='Users.staff'),
        ),
        migrations.AddField(
            model_name='ticketpicture',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='Ticket.ticket'),
        ),
    ]
