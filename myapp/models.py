from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Games(models.Model):
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=20)
    price = models.IntegerField()
    pimage=models.ImageField(upload_to='image')
    file_path = models.FileField(upload_to='game_files')


class Cart(models.Model):
    gid = models.ForeignKey(Games,on_delete=models.CASCADE,db_column='gid')
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    order_id = models.IntegerField()
    gid = models.ForeignKey(Games,on_delete=models.CASCADE,db_column='gid') 
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity = models.IntegerField(default=1)
    token = models.CharField(max_length=255, blank=True, null=True)