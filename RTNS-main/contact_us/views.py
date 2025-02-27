from django.shortcuts import render
from contact_us.models import Contact_Us
# Create your views here.
def Contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
        contact=Contact_Us()
        contact.name=name
        contact.email=email
        contact.subject=subject
        contact.message=message
        contact.save()
    return render(request,"core/contact.html")