from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_auth.models import User
from .models import Profile
import re

class UserRegisterForm(UserCreationForm):
    name=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name","class":"form-control sign_up_form_group"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email","class":"form-control"}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password","class":"form-control"}))
    class Meta:
        model= User
        fields=['name','email']
    def clean(self):
        clean_data=super().clean()
        name=clean_data.get('name')
        if not re.match(r'^[a-zA-Z\s]+$', name):
            self.add_error('name','Name must contain only alphabets.') 
        if len(name) < 3:
            self.add_error('name',"Name must be at least 3 characters long.")
        if len(name) > 30:
            self.add_error('name',"Name cannot exceed 30 characters.")  
    

class UserUpdateForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name","class":"form-control sign_up_form_group"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email","class":"form-control"}))
    class Meta:
        model=User
        fields=['name','email']    

class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control mb-3"}))
    class Meta:
        model=Profile
        fields=['image']
