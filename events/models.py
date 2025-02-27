from datetime import datetime, timezone 
from django.db import models
from user_auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from speakers.models import *
# Create your models here.

class Event(models.Model):
    Event_type_Choice=[
        ('physical','Physical'),
        ('online','Online')
    ]
    title=models.CharField(max_length=100,)
    date=models.DateField(default=datetime(2023,10,11),blank=True)
    event_type=models.CharField(max_length=10,choices=Event_type_Choice)

    def __str__(self):
        return self.title

class Speech(models.Model):
    event=models.ForeignKey('Event',on_delete=models.CASCADE)
    start_time = models.TimeField(blank=True,null=True)
    end_time=models.TimeField(blank=True,null=True)
    speech_title=models.CharField(max_length=300)
    speaker=models.ForeignKey(Speaker,blank=True,null=True,on_delete=models.CASCADE)
    session_chair=models.CharField(max_length=300)
    def __str__(self):
        return f"{self.event.title} - {self.speech_title}"
class LiveStream(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    stream_url = models.URLField()
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.event.title} - Live Stream"
    
class Message(models.Model):
    live_stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message: {self.text[:50]}"

    class Meta:
        ordering = ['-timestamp']
        
        



                
                
                
class Area(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class SubArea(models.Model):
    name=models.CharField(max_length=100)
    purpose=models.ForeignKey('Area',on_delete=models.CASCADE,)
    def __str__(self):
        return self.name
    
class EventReg(models.Model):
    AREA_CHOICES = [
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
    ]

    DESIGNATION_CHOICES = [
        ('Faculty', 'Faculty'),
        ('Student', 'Student'),
        ('Others', 'Others'),
    ]

    FACULTY_DESIGNATION_CHOICES = [
        ('Lecturer', 'Lecturer'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
    ]

    HOW_HEAR_CHOICES = [
        ('Social Media', 'Social Media'),
        ('Email', 'Email'),
        ('Word of Mouth', 'Word of Mouth'),
        ('Other', 'Other'),
    ]

    PURPOSE_CHOICES = [
        ('Abstract Submission', 'Abstract Submission'),
        ('Poster Submission', 'Poster Submission'),
        ('Only Attending', 'Only Attending'),
    ]

    REGISTRATION_TYPE_CHOICES = [
        ('Regular Registration', 'Regular Registration'),
        ('Student Registration', 'Student Registration'),
    ]
    VERIFIED_CHOICES = [
        ('Approved for Submission', 'Approved for Submission'),
        ('Approved for Presentation', 'Approved for Presentation'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    ]
    ABSTRACT_CATEGORY_CHOICES=[
        ('Oral Presentation','Oral Presentation'),
        ('Poster Presentation','Poster Presentation')
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    area = models.CharField(max_length=255, choices=AREA_CHOICES)
    designation = models.CharField(max_length=255, choices=DESIGNATION_CHOICES)
    faculty_designation = models.CharField(max_length=255, choices=FACULTY_DESIGNATION_CHOICES)
    affiliation = models.CharField(max_length=255)
    fee_receipt = models.FileField(upload_to='fee_receipts',null=True,blank=True)
    registration_type = models.CharField(max_length=255, choices=REGISTRATION_TYPE_CHOICES)
    how_hear = models.CharField(max_length=255, choices=HOW_HEAR_CHOICES)
    terms_and_conditions = models.BooleanField()
    purpose = models.ForeignKey('Area',on_delete=models.SET_NULL,null=True,blank=True)
    purposetype = models.ForeignKey('SubArea',on_delete=models.SET_NULL,null=True,blank=True)
    status = models.CharField(choices=VERIFIED_CHOICES,default='Pending',max_length=100)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        original_instance = None
        if self.pk:
            original_instance = EventReg.objects.get(pk=self.pk)
        super(EventReg, self).save(*args, **kwargs)
        if original_instance and original_instance.approved != self.approved:
            if self.approved == 'Approved':
                send_mail(
                    'Event Registration Approved',
                    'Your registration has been approved. Thank you for registering for the event!',
                    settings.EMAIL_HOST_USER,
                    [self.email],
                    fail_silently=True,
                )
            elif self.approved == 'Rejected':
                send_mail(
                    'Event Registration Rejected',
                    'We regret to inform you that your registration has been rejected.',
                    settings.EMAIL_HOST_USER,
                    [self.email],
                    fail_silently=True,
                )
                
                
