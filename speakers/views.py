from django.shortcuts import render
from .models import *
# Create your views here.
def Spekaers(request):
    n_speakers=Speaker.objects.filter(speaker_type='national')
    I_speakers=Speaker.objects.filter(speaker_type='international')
    context={
            'n_speakers':n_speakers,
            'I_speakers':I_speakers
        }
    return render(request,'core/speakers.html',context)