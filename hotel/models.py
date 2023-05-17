from PIL import Image
from django.db import models
import datetime
import os

# Create your models here.
def get_image(instance, filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s' % (current_time, old_name)
    return os.path.join('idproof', filename)

class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone_no = models.BigIntegerField()
    password = models.CharField(max_length=150)
    c_idproof = models.ImageField(upload_to=get_image, blank=True)

    def save(self, *args, **kwargs):
        # Call save() function of the superclass
        super().save(*args, **kwargs)

        # Resize the image after saving
        if self.c_idproof:
            img = Image.open(self.c_idproof.path)
            max_size = (800, 600)
            img.thumbnail(max_size)
            img.save(self.c_idproof.path)

    def __str__(self):
        return self.name


class rating(models.Model):
    cust_name = models.ForeignKey(Customer, on_delete = models.CASCADE)
    review = models.CharField(max_length=200, blank=True)
    rating = models.PositiveIntegerField()
