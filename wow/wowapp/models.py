from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    price=models.FloatField()
    is_active=models.BooleanField(default=True)
    pimages=models.ImageField(upload_to='image')
    def __str__(self):
        return self.name
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
class Orders(models.Model):
    orderId=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)