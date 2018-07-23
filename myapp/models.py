from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.



class Customer(models.Model):

    friendly_name = models.CharField(max_length=128)
    name_on_card = models.ForeignKey(User,on_delete=models.CASCADE)
    expiry_date = models.DateField()
    type_of_card = models.CharField(max_length=50)
    cvv = models.IntegerField()
    card_no=models.CharField(max_length=20)


    def __str__(self):
        return self.name_on_card
