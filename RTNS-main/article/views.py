from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import docx

import mimetypes

from docx import Document
from django.core.mail import send_mail
from django.conf import settings
from mammoth import convert_to_html
from event_reg.models import *
# Create your views here.


def AprovedArticles(request):
    approvedarticles = Event_Registration.objects.filter(
    status__in=['approveforpresentation', 'approveforposter'])
    for article in approvedarticles:
        document = docx.Document(article.abstract_file.path)
        article.content = "\n".join([paragraph.text for paragraph in document.paragraphs])
        article.save()
    context={
        'approved_articles':approvedarticles,
    }
    return render(request,'core/articles.html',context)

def SingleArticle(request,article_id):
    article=get_object_or_404(Event_Registration,pk=article_id)
    with open(article.abstract_file.path,'rb') as docx_file:
        html_file=convert_to_html(docx_file)
        html_content=html_file.value
    
    context={
        'article':article,
        'html_content':html_content
    }
    return render(request,'core/single_article.html',context)


