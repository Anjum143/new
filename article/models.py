from django.db import models
from user_auth.models import User,Profile
from events.models import Event
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    article_file=models.FileField(upload_to='article/article_files/')
    content=models.TextField(null=True,blank=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        original_instance = None
        if self.pk:
            original_instance = Article.objects.get(pk=self.pk)
        super(Article, self).save(*args, **kwargs)
        if original_instance and original_instance.status != self.status:
            if self.status == 'Approved':
                send_mail(
                    'Article Approved',
                    'Your Article has been approved. Thank you for sharing Article!',
                    settings.EMAIL_HOST_USER,
                    [self.author.email],
                    fail_silently=True,
                )
            elif self.status == 'Rejected':
                send_mail(
                    'Article Rejected',
                    'Your Article has been rejected.',
                    settings.EMAIL_HOST_USER,
                    [self.author.email],
                    fail_silently=True,
                )