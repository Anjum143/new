from django.urls import path
from .views import *


app_name="partials"

urlpatterns=[
    path("header",HeaderFooterView,name="header"),
    # path('ajax/load-subarea/',load_subarea, name='ajax_load_subarea'),
    
]