# Generated by Django 5.0.1 on 2024-02-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0011_alter_staff_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='device_reg_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]