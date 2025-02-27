from django.db import models

# Create your models here.
class Speaker(models.Model):
    SPEAKER_TYPE_CHOICES = [
        ('national', 'National'),
        ('international', 'International'),
    ]

    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='speakers/national_speakers/')
    designation=models.CharField(max_length=300)
    email=models.EmailField(blank=True,null=True)
    speaker_type=models.CharField(max_length=30,choices=SPEAKER_TYPE_CHOICES,blank=True,null=True) 

    def __str__(self):
        return self.name
    
