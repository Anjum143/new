from django.db import models
from user_auth.models import User,Profile
from events.models import Event
# Create your models here.
class Contact_Us(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    subject=models.CharField(max_length=100)
    message=models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.title