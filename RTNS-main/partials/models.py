from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import admin

class WebsiteHeader(models.Model):
    rtns_logo = models.ImageField(upload_to='header',default='static/Image/RTNSlogo.png')
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
    logo = models.ImageField(upload_to='header/department_logos')
        
   
def max_sponsor_logos(value):
    footer = value.instance.footer
    if footer.sponsor_logos.count() >= 2:
        raise ValidationError("Maximum of 2 sponsor logos are allowed.")


     
class WebsiteFooter(models.Model):
    title=models.CharField(max_length=4,default='RTNS')
    year=models.IntegerField(default=2024)
    contact=models.CharField(max_length=13)
    email=models.EmailField(default='rtns@gmail.com')
    
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

class SponsorLogo(models.Model):
    footer = models.ForeignKey(WebsiteFooter, on_delete=models.CASCADE, related_name='sponsor_logos')
    image = models.ImageField(upload_to="images/footer", validators=[max_sponsor_logos])