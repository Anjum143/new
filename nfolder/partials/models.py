from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import admin

class WebsiteHeader(models.Model):
    rtns_logo = models.ImageField(upload_to='images/header',default='static/Image/RTNSlogo.png')
    title = models.CharField(max_length=100, default="International Conference on Recent Trends in Natural Sciences")

    def save(self, *args, **kwargs):
        if not self.pk and WebsiteHeader.objects.exists():
            raise ValidationError("Only one instance of Header is allowed.")
        return super().save(*args, **kwargs)

    

    @classmethod
    def get_instance(cls):
        header_instance, _ = cls.objects.get_or_create(pk=1)
        return header_instance

class DepartmentLogo(models.Model):
    header = models.ForeignKey(WebsiteHeader, on_delete=models.CASCADE, related_name='department_logos')
    logo = models.ImageField(upload_to='images/header/department_logos')

    def clean(self):
        if self.header.department_logos.count() >= 4:
            raise ValidationError("Only 4 DepartmentLogos are allowed per Header.")
    def delete(self, *args, **kwargs):
        pass    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
        
class WebsiteFooter(models.Model):
    title=models.CharField(max_length=4,default='RTNS')
    year=models.IntegerField(default=2024)
    contact=models.CharField(max_length=13)
    email=models.EmailField(default='rtns@gmail.com')
    sponsor_logo=models.ImageField(upload_to="images/footer",default='static/Image/ue.png')
    
    def save(self, *args, **kwargs):
        if not self.pk and WebsiteFooter.objects.exists():
            raise ValidationError("Only one instance of Footer is allowed.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get_instance(cls):
        footer_instance, _ = cls.objects.get_or_create(pk=1)
        return footer_instance

