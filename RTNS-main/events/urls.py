from django.urls import path
from .views import *


app_name="events"

urlpatterns=[
    path("events",Events,name="events"),
    # path('live-stream/<int:event_id>/', live_stream, name='live_stream'),
    # path('live-stream/<int:event_id>/post-message/', post_message, name='post_message'),
    
]