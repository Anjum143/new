from django.shortcuts import render
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.shortcuts import render,redirect
from django.conf import settings
from .forms import *
from googleapiclient.http import MediaFileUpload
import os
from django.contrib import messages
import mimetypes
from googleapiclient.http import MediaFileUpload
import tempfile
from PIL import Image
from django.shortcuts import render, get_object_or_404
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import io 
from .models import Event_Registration
from django.core.mail import send_mail
from django.urls import reverse

# Create your views here.

def get_file_name(category):
    registrations = Event_Registration.objects.filter(abstract_category=category)
    count = registrations.count() + 1
    file_name = f"{category}_{count:03d}.docx"
    return file_name

def verify_image_type(image_file):
    try:
        img = Image.open(image_file)
        img.verify()
        return True
    except (IOError, SyntaxError):
        return False
    
def event_submission(request):
    try:
        if request.method == 'POST':
            form = Event_RegForm(request.POST, request.FILES)
            print("errors are",form.errors)
            if form.is_valid():
                print("form is valid")
                reg_model = form.save(commit=False)
                user_name=form.cleaned_data['name']
                if 'fee_receipt' in request.FILES:
                    print("find the recpt")
                    fee_receipt=request.FILES['fee_receipt']
                    # print(verify_image_type(fee_receipt))
                    filemimetype, _ = mimetypes.guess_type(fee_receipt.name)
                    print("type is",filemimetype)
                    allowed_mimetypes = ['image/jpeg', 'image/jpg']
                    print("type is",filemimetype)
                    if filemimetype not in allowed_mimetypes:
                        messages.error(request,'Please upload a JPG or JPEG image of fee_receipt.')
                        return render(request, 'core/eventregistration.html',{'form':form})
                    else:
                        
                        print("hello")
                
                if reg_model.reg_purpose == 'abstract':
                    category=reg_model.abstract_category
                    file = request.FILES['abstract_file']
                    print("file is",file)
                    if file:
                        print(file.name)
                        file_mime_type, encoding = mimetypes.guess_type(file.name)
                        allowed_mime_types = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']
                        if file_mime_type not in allowed_mime_types:
                            print('not equal')
                            messages.error(request, 'Invalid file type. Please submit a valid .docx abstract file.')
                            return render(request, 'hello.html', {'form':form})
                        else:
                            file.name = get_file_name(category)
                            file_id = upload_to_google_drive(file)
                            reg_model.file_id = file_id
                    reg_model.save()
                    admin_panel_url = request.build_absolute_uri(reverse('admin:index'))
                    subject="New Registration Request"
                    message=f"A new registration request has been submitted.{admin_panel_url}"
                    from_email=settings.EMAIL_HOST_USER
                    to_email=[settings.ADMIN_EMAIL]
                    
                    send_mail(subject,message,from_email,to_email,fail_silently=True)
                    form=Event_RegForm()
                    messages.success(request,'Your application has been submitted successfully, you will be informed soon via email')
                    return redirect('')
                else:
                    reg_model.save()
                    admin_panel_url = request.build_absolute_uri(reverse('admin:index'))
                    subject="New Registration Request"
                    message=f"A new registration request has been submitted.{admin_panel_url}"
                    from_email=settings.EMAIL_HOST_USER
                    to_email=[settings.ADMIN_EMAIL]
                    
                    send_mail(subject,message,from_email,to_email,fail_silently=True)
                    form=Event_RegForm()
                    messages.success(request,'Your application has been submitted successfully, you will be informed soon via email')
                    return redirect('')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"{field}: {error}") 
                return render(request, 'core/eventregistration.html',{'form':form})
    # Save the form data to the database
                # Redirect to a success page
        else:
            print('yes')
            form = Event_RegForm()
    except Exception as e:
        print("error is",e)
    
    data=Event_Registration.objects.all()
    form=Event_RegForm()
    return render(request, 'core/eventregistration.html', {'form' : form,'data':data})

def upload_to_google_drive(file_data):
    # Authenticate with Google Drive API
    credentials = service_account.Credentials.from_service_account_file(settings.GOOGLE_DRIVE_CREDENTIALS)
    drive_service = build('drive', 'v3', credentials=credentials)

    # Save the file to a temporary location on disk
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_data.read())
        temp_file.flush()

        file_metadata = {
            'name': file_data.name,
            'parents': ['1ATqBLQDirVyNRgTXmSMkLFBnXC4sr-s9']
        }
        media = MediaFileUpload(temp_file.name, mimetype=file_data.content_type)
        uploaded_file= drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Delete the temporary file
    try:
        os.remove(temp_file.name)
    except OSError:
        pass
    
    return uploaded_file.get('id')


def load_subarea(request):
    area_id = request.GET.get('area_id')
    subarea = SubArea.objects.filter(area_id=area_id).all()
    return render(request, 'core/selectedsubarea.html', {'subarea': subarea})
    return JsonResponse(list(cities.values('id', 'name')), safe=False)
