from django.db import models
from datetime import datetime
from realtors.models import Realtor
from django.contrib.auth.models import User, AbstractUser,BaseUserManager

class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField(default=1)
    floorcount = models.IntegerField(blank=True,default=1)
    floornumber = models.IntegerField(blank=True,default=1)
    builddate = models.IntegerField(default=2019,blank=True)
    livingroom = models.IntegerField(blank=True,default=1)
    heating =models.IntegerField(default=0, blank=True)
    frontage=models.IntegerField(default=0, blank=True)
    elevator=models.IntegerField(default=0, blank=True)
    heatIsolation=models.IntegerField(blank=True,default=0)
    garage = models.IntegerField(default=0,blank=True)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.title