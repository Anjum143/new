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
# class LiveStream(models.Model):
#     event = models.OneToOneField(Event, on_delete=models.CASCADE)
#     stream_url = models.URLField()
#     start_time = models.DateTimeField(default=datetime.now)
#     end_time = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.event.title} - Live Stream"
    
# class Message(models.Model):
#     live_stream = models.ForeignKey(LiveStream, on_delete=models.CASCADE)
#     user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
#     text = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message: {self.text[:50]}"

#     class Meta:
#         ordering = ['-timestamp']
        
        



                
                
                
class Area(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class SubArea(models.Model):
    name=models.CharField(max_length=100)
    purpose=models.ForeignKey('Area',on_delete=models.CASCADE,)
    def __str__(self):
        return self.name
    

                
