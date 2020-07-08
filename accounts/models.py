from django.contrib.auth.models import User, AbstractUser,BaseUserManager
from django.db import models

class extenduser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=300)