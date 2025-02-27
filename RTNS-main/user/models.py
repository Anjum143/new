from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from PIL import Image
# User=settings.AUTH_USER_MODEL
# Create your models here.
class Users(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100,unique=False)
    image=models.ImageField(upload_to="Profile/Profile_images/",blank=True,null=True)
    verified=models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.username
    
    
    
    
class Profiles(models.Model):
    user=models.OneToOneField(Users,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="Profile/Profile_images/",blank=True,null=True)
    verified=models.BooleanField(default=False)
    
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img=Image.open(self.image.path)

            if img.width > 300 or img.height > 300:
                output_size=(300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    
