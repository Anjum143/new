from django.shortcuts import render
from .models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def HeaderView(request):
    try:
        header_data=WebsiteHeader.objects.get()
    except ObjectDoesNotExist:
        header_data=None
        
    print("head is",header_data)
    content={
        'header':header_data
    }  
    return render(request,'partials/base.html',content)
        
