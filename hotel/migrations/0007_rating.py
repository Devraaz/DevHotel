# Generated by Django 4.0.6 on 2023-05-17 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_alter_customer_c_idproof'),
    ]

    operations = [
        migrations.CreateModel(
            name='rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(blank=True, max_length=200)),
                ('rating', models.PositiveIntegerField()),
                ('cust_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.customer')),
            ],
        ),
    ]
