from django import forms
from django.core.validators import FileExtensionValidator
from .models import Article
from events.models import Event

class ArticleSubmissionForm(forms.ModelForm):

    title=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Title","class":"form-control sign_up_form_group"}))
    author=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Author","class":"form-control sign_up_form_group"}))
    article_file=forms.FileField(widget=forms.FileInput(attrs={"class":"form-control sign_up_form_group"}))
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        widget=forms.Select(attrs={"class": "form-control sign_up_form_group"})
    )
    class Meta:
        model=Article
        fields=['title','article_file','event']
        validators=[FileExtensionValidator(allowed_extensions=['docx'])]

class ArticleFilterForm(forms.Form):
    status_choices=[
        ('','------'),
        ('pending','Pending'),
        ('rejected','Rejected'),
        ('approved','Approved')
    ]
    status=forms.ChoiceField(choices=status_choices,label='Filter by Status',required=False,widget=forms.Select(attrs={"class":"form-control filter-form-control"}))


        