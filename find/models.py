from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mechanic(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    shop_name=models.CharField(max_length=250)
    phone_number=models.CharField(max_length=10)
    address=models.TextField()
    lattitude=models.CharField(max_length=25)
    longitude=models.CharField(max_length=25)
    about=models.TextField()
    def __str__(self):
        return self.shop_name
