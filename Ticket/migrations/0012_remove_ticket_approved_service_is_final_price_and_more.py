# Generated by Django 5.0.1 on 2024-02-15 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0011_service_type_ticket_info_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='approved',
        ),
        migrations.AddField(
            model_name='service',
            name='is_final_price',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='location',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Rejected', 'Rejected by company'), ('Pending', 'Pending for client approval'), ('Client Rejected', 'Rejected by client'), ('In Progress', 'In Progress'), ('Closed', 'Closed'), ('Rated', 'Rated')], default='Open', max_length=20),
        ),
    ]