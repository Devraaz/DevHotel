from django.db import models
import datetime, os

# Create your models here.
def get_image(instance, filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s'%(current_time, old_name)
    return os.path.join('idproof', filename)


class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_no = models.BigIntegerField()
    password = models.CharField(max_length=150)

    
    c_idproof = models.ImageField(upload_to = get_image, blank=True )
    def __str__(self):
        return self.name
    

