from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager
import uuid
from django.conf import settings
from PIL import Image

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100,default='hamza',null=True,blank=True,unique=False)
    image=models.ImageField(upload_to="Profile/Profile_images/",blank=True,null=True)
    verified=models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    objects=UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.username
    
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
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
    
    