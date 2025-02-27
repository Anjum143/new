from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/')

class AboutUs(models.Model):
    about_heading=models.CharField(max_length=100,default='What is RTNS')
    content = models.TextField()
    image = models.ImageField(upload_to='about_us/')
    
    def save(self, *args, **kwargs):
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError("Only one instance of Header is allowed.")
        return super().save(*args, **kwargs)

class Patron(models.Model):
    name=models.CharField(max_length=100)
    patron_type=models.CharField(max_length=100,default='Patron')
    designation=models.CharField(max_length=300)
    image = models.ImageField(upload_to='patrons/')
    
    
    
class Gallery(models.Model):
    image=models.ImageField(upload_to='Gallery/')