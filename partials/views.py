from django.shortcuts import render
from .models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def HeaderFooterView(request):
    try:
        header_data=WebsiteHeader.objects.get()
        footer_data=WebsiteFooter.objects.get()
        dep_logo=DepartmentLogo.objects.all()
        sponsor_logo=SponsorLogo.objects.all()
    except ObjectDoesNotExist:
        header_data=None    
    content={
        'header':header_data,
        'footer':footer_data,
        'dep_logos':dep_logo,
        'sponsor_logo':sponsor_logo
    }  
    return render(request,'partials/base.html',content)