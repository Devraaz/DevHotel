# Generated by Django 4.0.6 on 2023-05-08 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_booking_history_book_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='room_details',
            name='book_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
