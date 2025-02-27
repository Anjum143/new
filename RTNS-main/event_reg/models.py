from django.db import models
from events.models import * 
# Create your models here.

class Area(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class SubArea(models.Model):
    name=models.CharField(max_length=100)
    area=models.ForeignKey('Area',on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Event_Registration(models.Model):
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('approveforposter', 'Approved for poster'),
        ('approveforpresentation', 'Approved for presentation'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    area = models.ForeignKey('Area',on_delete=models.SET_NULL,null=True,blank=True)
    registration_type = models.CharField(max_length=20, choices=(('regular_reg', 'Regular Registration'), ('student_reg', 'Student Registration')))
    designation = models.CharField(max_length=20)
    faculty_designation = models.CharField(max_length=20)
    affiliation = models.CharField(max_length=100)
    fee_receipt_id = models.CharField(max_length=255,blank=True,null=True)
    fee_receipt = models.FileField(upload_to='fee_receipts',blank=True,null=True)
    how_here = models.CharField(max_length=100)
    reg_purpose = models.CharField(max_length=20)
    
    abstract_name = models.CharField(max_length=100, blank=True)
    abstract_type = models.CharField(max_length=20, choices=(('oralpresentation', 'Oral presentation'), ('posterpresentation', 'Poster presentation')), blank=True)
    abstract_category = models.ForeignKey('SubArea',on_delete=models.SET_NULL,null=True,blank=True)
    file_id = models.CharField(max_length=255,blank=True,null=True)
    abstract_file=models.FileField(blank=True,null=True)
    keywords = models.CharField(max_length=200, blank=True)
    
    poster_title = models.CharField(max_length=100, blank=True)
    
    terms_conditions = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,default='pending')
    reason=models.TextField(blank=True,null=True)
    