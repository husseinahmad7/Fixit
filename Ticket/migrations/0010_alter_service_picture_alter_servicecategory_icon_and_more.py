# Generated by Django 5.0.1 on 2024-02-12 12:24

import gdstorage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0009_rename_discription_ticket_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='picture',
            field=models.ImageField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='serv_pictures/'),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='icon',
            field=models.ImageField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='cat_icons/'),
        ),
        migrations.AlterField(
            model_name='ticketpicture',
            name='picture',
            field=models.ImageField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='attachments/'),
        ),
    ]