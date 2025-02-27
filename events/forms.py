from .models import *
from django import forms
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventReg
        exclude = ['status']
