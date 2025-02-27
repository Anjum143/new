from django import forms
from .models import *
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django import forms
import re


class Event_RegForm(forms.ModelForm):
    AREA_CHOICES = (
        ('','-------'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('bio', 'Biology'),
    )

    DESIGNATION_CHOICES = (
        ('','-------'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('others', 'Others'),
    )
    
    FAC_DESIGNATION_CHOICES = (
        ('','-------'),
        ('lecturer', 'Lecturer'),
        ('assistant_professor', 'Assistant Professor'),
        ('associate_professor', 'Associate Professor'),
        ('professor', 'Professor'),
    )
    REG_TYPE=(
        ('','-------'),
        ('regular_reg', 'Regular Registration'),
        ('student_reg', 'Student Registration')
    )
    
    REG_PURPOSE_CHOICES = (
        ('attend', 'For only attending'),
        ('abstract', 'For abstract Submission'),
        ('poster', 'For poster submission'),
    )
    ABSTRACT_TYPE=(
        ('','-------'),
        ('oralpresentation', 'Oral presentation'),
        ('posterpresentation', 'Poster presentation')
    )
    ABSTRACT_CATEGORY=(
        ('','-------'),
        ('physics', 'Physics'), 
        ('chemistry', 'Chemistry'),
        ('bio', 'Biology')
    )
    

    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your name","class":"form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Enter your Email","class":"form-control","readonly":"readonly"}))
    area = forms.ModelChoiceField(queryset=Area.objects.all())
    registration_type = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}),choices=REG_TYPE)
    designation = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}),choices=DESIGNATION_CHOICES)
    faculty_designation = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}),choices=FAC_DESIGNATION_CHOICES)
    affiliation = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"e.g. University, Organization","class":"form-control"}),max_length=100)
    fee_receipt = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}),required=False)
    how_here = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"e.g. Internet search, friend referral, social media","class":"form-control"}),max_length=100)
    reg_purpose = forms.ChoiceField(choices=REG_PURPOSE_CHOICES, widget=forms.RadioSelect)
    
    abstract_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter abstract name","class":"form-control"}),max_length=100, required=False)
    abstract_type = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}),choices=ABSTRACT_TYPE, required=False)
    abstract_category = forms.ModelChoiceField(queryset=SubArea.objects.all(),required=False)
    abstract_file = forms.FileField(required=False,widget=forms.FileInput(attrs={"class":"form-control"}))
    keywords=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"e.g. Zoology, Chemistry","class":"form-control"}),max_length=200,required=False)
    
    poster_title=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter poster title here","class":"form-control"}),max_length=100, required=False)
    
    terms_conditions = forms.BooleanField(required=True)
    reason = forms.CharField(widget=forms.Textarea(attrs={'style': 'resize: none;',"class":"form-control"}),required=False)
    
    class Meta:
        model = Event_Registration
        exclude = ['status']
        validators=[FileExtensionValidator(allowed_extensions=['docx'])]
        
        
    def clean(self):
        clean_data=super().clean()
        name=clean_data.get('name')
        email=clean_data.get('email')
        if not re.match(r'^[a-zA-Z\s]+$', name):
            self.add_error('name','Name must contain only alphabets.') 
        if len(name) < 3:
            self.add_error('name',"Name must be at least 3 characters long.")
        if len(name) > 30:
            self.add_error('name',"Name cannot exceed 30 characters.")
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if not email:
            raise forms.ValidationError('This field is required.')
        
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['abstract_category'].queryset = SubArea.objects.none()

        if 'area' in self.data:
            try:
                area_id = int(self.data.get('area'))
                self.fields['abstract_category'].queryset = SubArea.objects.filter(area_id=area_id).order_by('name')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['abstract_category'].queryset = self.instance.area.subarea_set.order_by('name')     
        
    def clean_fee_receipt(self):
        fee_receipt = self.cleaned_data.get('fee_receipt')
        if fee_receipt:
            allowed_mimetypes = ['image/jpeg', 'image/jpg']
            file_mimetype = fee_receipt.content_type
            if file_mimetype not in allowed_mimetypes:
                raise ValidationError('Please upload a JPG or JPEG image for the fee receipt.')
        return fee_receipt
        
        

