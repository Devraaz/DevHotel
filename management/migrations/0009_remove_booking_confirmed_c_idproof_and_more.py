# Generated by Django 4.0.6 on 2023-05-06 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_payments_alter_pending_bookings_payment_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_confirmed',
            name='c_idproof',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='razorpay_signature_id',
        ),
    ]
