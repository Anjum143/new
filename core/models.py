from django.db import models

# Create your models here.
class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/')

class AboutUs(models.Model):
    about_heading=models.CharField(max_length=100,default='What is RTNS')
    content = models.TextField()
    image = models.ImageField(upload_to='about_us/')

class Patron(models.Model):
    name=models.CharField(max_length=100)
    patron_type=models.CharField(max_length=100,default='Patron')
    designation=models.CharField(max_length=300)
    image = models.ImageField(upload_to='patrons/')
    
    
class EmailConfiguration(models.Model):
    smtp_host = models.CharField(max_length=255)
    smtp_port = models.IntegerField()
    admin_email = models.EmailField()
    password = models.CharField(max_length=255)
    
class Gallery(models.Model):
    image=models.ImageField(upload_to='Gallery/')