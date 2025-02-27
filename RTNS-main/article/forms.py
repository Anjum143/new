from django import forms
from django.core.validators import FileExtensionValidator

from events.models import Event



class ArticleFilterForm(forms.Form):
    status_choices=[
        ('','------'),
        ('pending','Pending'),
        ('rejected','Rejected'),
        ('approveforposter','Approve for poster'),
        ('approveforpresentation','Approve for presentation')
    ]
    status=forms.ChoiceField(choices=status_choices,label='Filter by Status',required=False,widget=forms.Select(attrs={"class":"form-control filter-form-control"}))


        