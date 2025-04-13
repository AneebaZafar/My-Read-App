from django.db import models
from django.core.validators import MinLengthValidator

class User(models.Model):
    user_id=models.AutoField
    name=models.CharField(max_length=50, default="", blank=True, null=True)
    email=models.CharField(max_length=50, default="", blank=True, null=True)
    password=models.CharField(max_length=5000, default="", blank=True, null=True)
    

    def __str__(self):
        return self.name

