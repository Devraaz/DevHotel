from django.db import models
from random import choices
from django.utils import timezone
import os, datetime


ROOMS_TYPE = (
    ('Single','Single'),
    ('Delux', 'Delux')
)
BOOKED = (
    ('Yes','Yes'),
    ('No', 'No')
)

def get_image(instance, filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s'%(current_time, old_name)
    return os.path.join('media/idproof', filename)


def get_file(instance, filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s'%(current_time, old_name)
    return os.path.join('media/booking', filename)


# Create your models here.
class staff_user(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length=150)

    address =models.CharField(max_length = 50)


    def __str__(self):
        return self.name
    
class room_details(models.Model):
    room_no = models.IntegerField()
    room_type = models.CharField(choices = ROOMS_TYPE, max_length=20)
    is_booked = models.CharField(choices = BOOKED, max_length = 20, default = 'No')
    checkInDate = models.DateField(default = None, null=True, blank = True)
    checkOutDate = models.DateField(default = None, null=True, blank = True)
    price = models.IntegerField()
    book_id = models.IntegerField(blank = True, null=True, default = None)

    def __str__(self):
        return str(self.room_no)

    def is_available(self, checkInDate, checkOutDate):
        """
        Check if the room is available between the given checkin and checkout dates.
        """
        if self.checkInDate is None or self.checkOutDate is None:
            return True
        elif checkInDate > self.checkOutDate or checkOutDate < self.checkInDate:
            return True
        else:
            return False


class booking(models.Model): 
    cust_name = models.CharField(max_length=50)
    cust_phone = models.BigIntegerField()
    cust_email = models.EmailField()
    cust_idproof = models.ImageField(upload_to = get_file, max_length=150, blank=True)
    room_no = models.PositiveIntegerField()
    room_type = models.CharField(max_length=10)
    checkin =models.DateField()
    checkout = models.DateField()
    is_booked = models.CharField(choices = BOOKED, max_length=10, default = 'No')   #Hidden
    price = models.PositiveIntegerField()
    
    payment_status = models.CharField(choices = BOOKED, max_length=10, default = 'No')   #hidden
    order_id = models.CharField(max_length = 100, blank=True )
    date = models.DateField()                 #hidden


    def __str__(self):
        return  self.cust_name
    
    def is_available(self, checkin, checkout):
            #if self.room_no == room_no
        print(checkin, self.checkin)
        print(checkout, self.checkout)

        if self.checkin is None or self.checkout is None:
            return True
        elif checkin > self.checkout or checkout < self.checkin:
            return True
        else:
            return False






class booking_history(models.Model):
    book_id = models.IntegerField(unique=True, null=True, blank=True)
    cust_name = models.CharField(max_length=50)
    cust_phone = models.BigIntegerField(null=True, blank=True)
    cust_email = models.EmailField()
    cust_idproof = models.ImageField(upload_to = get_file, max_length=150, blank=True)
    room_no = models.PositiveIntegerField()
    room_type = models.CharField(max_length=10)
    checkin =models.DateField(blank=True, null=True)
    checkout = models.DateField(blank=True, null=True)
    is_booked = models.CharField(choices = BOOKED, max_length=10, default = 'No')   #Hidden
    price = models.PositiveIntegerField()
    
    payment_status = models.CharField(choices = BOOKED, max_length=10, default = 'No')   #hidden
    order_id = models.CharField(max_length = 100, blank=True )
    checked_out = models.CharField(choices = BOOKED, max_length=10, default='No')
    date = models.DateField()

    def __str__(self):
        return  self.cust_name

class payments(models.Model):
    razorpay_order_id = models.CharField(max_length= 100, blank = True, null = True, unique=True)
    razorpay_payment_id = models.CharField(max_length= 100, blank = True, null = True)
    razorpay_signature = models.CharField(max_length= 100, blank = True, null = True)
    
    amount = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=10, default='No') # Payment status field
    customer_email = models.EmailField(max_length=50)
    def __str__(self):
        return self.customer_email

