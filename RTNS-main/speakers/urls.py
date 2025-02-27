from django.urls import path
from .views import *

app_name="speakers"

urlpatterns=[
    path("speakers",Spekaers,name="speakers")
    
    
]