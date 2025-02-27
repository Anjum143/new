from partials.models import *
from django.db import models

def header_context(request):
    header_context=WebsiteHeader.objects.first()
    return  {'header':header_context}

def footer_context(request):
    footer_context=WebsiteFooter.objects.first()
    return {'footer':footer_context}

def dep_logo(request):
    dep_logo=DepartmentLogo.objects.all().order_by('id')[:3] 
    return {'dep_logos':dep_logo}