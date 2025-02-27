from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import docx
from .forms import ArticleSubmissionForm
import mimetypes
from .models import Article
from docx import Document
from django.core.mail import send_mail
from django.conf import settings
from mammoth import convert_to_html

# Create your views here.
@login_required
def submit_article(request):
    text_content=''
    if request.method=="POST":
        form=ArticleSubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            article=form.save(commit=False)
            article.author=request.user

            file_mime_type, encoding = mimetypes.guess_type(article.article_file.name)
            allowed_mime_types = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            if file_mime_type not in allowed_mime_types:
                messages.error(request, 'Invalid file type. Please submit a valid .docx file.')
            else:
                article.status = 'pending'
                article.save()
                messages.success(request, 'Article submitted successfully!')
                form=ArticleSubmissionForm(initial={'author':request.user})
                

        else:
            messages.error(request, 'Invalid form submission. Please check the form and try again.')
    else:
        form = ArticleSubmissionForm(initial={'author':request.user})
    return render(request, 'core/submit_article.html', {'form': form}) 


def AprovedArticles(request):
    approvedarticles=Article.objects.all()
    for article in approvedarticles:
        document = docx.Document(article.article_file.path)
        article.content = "\n".join([paragraph.text for paragraph in document.paragraphs])
        article.save()
        if article.status == 'approved':
            print('approved')
            subject = 'Your Article has been Approved'
            message = f'Congratulations! Your article "{article.title}" has been approved.'
        elif article.status == 'rejected':
            print('not send')
            subject = 'Article Submission Update'
            message = f'Sorry, your article "{article.title}" has been rejected.'

        # send_mail(subject, message, settings.EMAIL_HOST_USER, [article.author.email])
    context={
        'approved_articles':approvedarticles,
    }
    return render(request,'core/articles.html',context)

def SingleArticle(request,article_id):
    article=get_object_or_404(Article,pk=article_id)
    with open(article.article_file.path,'rb') as docx_file:
        html_file=convert_to_html(docx_file)
        html_content=html_file.value
    
    context={
        'article':article,
        'html_content':html_content
    }
    return render(request,'core/single_article.html',context)


