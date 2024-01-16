# Generated by Django 5.0.1 on 2024-01-15 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0008_service_picture_servicecategory_icon'),
        ('Users', '0007_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='skills',
        ),
        migrations.AddField(
            model_name='staff',
            name='services',
            field=models.ManyToManyField(blank=True, to='Ticket.service'),
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]