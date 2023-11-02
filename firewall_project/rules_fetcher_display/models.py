from django.db import models
# Create your models here.
class prerouting(models.Model):
    routing = models.CharField(max_length=10)
    source_ip = models.CharField(max_length=18)
    source_port = models.CharField(max_length=6)
    protocol = models.CharField(max_length=3)
    destination_ip = models.CharField(max_length=18)
    destination_port = models.CharField(max_length=3)

class postrouting(models.Model):
    routing = models.CharField(max_length=10)
    source_ip = models.CharField(max_length=18)
    destination_ip = models.CharField(max_length=18)


'''
USER AUTH
'''
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        permissions = [
            ("view", "Can view page"),
            ("edit", "Can edit pages"),
        ]

'''
SERVER LOGIN
'''
from django.db import models

class encryptdata(models.Model):
    encryptdata_field= models.BinaryField()