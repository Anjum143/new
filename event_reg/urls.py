from django.urls import path
from .views import *


app_name="event_reg"

urlpatterns=[
    path("registration",event_submission,name="registration"),
    path('ajax/load-subarea/',load_subarea, name='ajax_load_subarea'),
    
]