from django.shortcuts import render
from events.models import *
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from .models import *
# Create your views here.
from datetime import datetime, timedelta

from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import SliderImage, AboutUs, Patron, Gallery
from events.models import Event, Speech


# Create your views here.

def index(request):
    today = date.today()
    try:
        slider_images = SliderImage.objects.all()
        about_us = AboutUs.objects.first()
        patron = Patron.objects.all()
        gallery = Gallery.objects.all()

        upcoming_event = Event.objects.filter(date__gte=today).order_by('date').first()

        if upcoming_event:
            first_speech = Speech.objects.filter(event=upcoming_event).order_by('start_time').first()
            if first_speech:
                event_date_formatted = upcoming_event.date.strftime("%Y-%m-%d")
                event_time = first_speech.start_time.strftime("%H:%M:%S")
                event_datetime = datetime.combine(upcoming_event.date, first_speech.start_time)
                current_datetime = datetime.now()
                remaining_days = (event_datetime - current_datetime).days
                context = {
                    'event_date_formatted': event_date_formatted,
                    'event_time': event_time,
                    'remaining_days': remaining_days,
                }
                
            else:
                context = {}
        else:
            context = {}

        home_content = {
            'slider_images': slider_images,
            'about_us': about_us,
            'patron': patron,
            'gallery': gallery,
        }
        print("conte2",context)
        return render(request, 'core/index.html', {**home_content, **context})
    except ObjectDoesNotExist:
        return render(request, 'core/index.html', {})