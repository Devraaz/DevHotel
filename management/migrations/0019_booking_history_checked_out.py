# Generated by Django 4.0.6 on 2023-05-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0018_rename_c_email_booking_history_cust_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_history',
            name='checked_out',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10),
        ),
    ]
