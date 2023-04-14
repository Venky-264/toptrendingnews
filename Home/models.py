from django.db import models

# Create your models here.
class Register(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    interest=models.CharField(max_length=20)

