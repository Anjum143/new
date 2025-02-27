from django.shortcuts import render,redirect
from user_auth.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.contrib import messages
from django.contrib.messages import constants
from django.conf import settings
from user_auth.models import Profile,User

from article.forms import ArticleFilterForm
from .forms import ProfileUpdateForm,UserUpdateForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from partials.models import *
from event_reg.models import *


def sign_up(requst):
    password_warnings=["Atleast 8 characters.",
                       "Not include username.",
                       "Don't use common password."]
    websitelogo=WebsiteHeader.objects.first().rtns_logo
    if requst.method =="POST":
        form = UserRegisterForm(requst.POST or None)
        if form.is_valid():
            form.save(commit=False)
            email=form.cleaned_data.get("email")
            name=form.cleaned_data.get("name")
            password=form.cleaned_data.get("password1")
            email_token=str(uuid.uuid4())
            hashed_password = make_password(password)
            user = User.objects.create(email=email,password=hashed_password,username=name,email_verification_token=email_token)
            user.save()
            send_email_after_registration(email,email_token,requst)
            return redirect('user_auth:token_send')
    else:
        form=UserRegisterForm()      
    context={
        'websitelogo':websitelogo,
        'form':form,
        'password_warnings':password_warnings
    }
    return render(requst,"user_auth/sign_up.html",context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,"Hey,You are already logged In")
        return redirect("user_auth:user_dashboard")   

    if request.method == "POST":
        email=request.POST.get("email")
        password = request.POST.get("password")

        try:
            user=User.objects.get(email=email)
        except:
            messages.warning(request,"")

        user=authenticate(request,email=email,password=password)
        if user is not None:
            if user.verified:
                login(request,user)
                messages.success(request,"You are logged in")
                return redirect("user_auth:user_dashboard")
            else:
                messages.warning(request,"Please verify your Email to Login.")
                return redirect('user_auth:user_signin')
        else:
            if User.objects.filter(email=email):
                messages.error(request,f"Email or Password is incorrect")
                return redirect('user_auth:user_signin')
            else:
                messages.error(request,"No account for this email,Please register first")
            return redirect('user_auth:user_signup')
    is_sign_in_page = True
    websitelogo=WebsiteHeader.objects.first().rtns_logo
    contaxt={
        'websitelogo':websitelogo,
        'is_sign_in_page' :is_sign_in_page
    }   

    return render(request,"user_auth/sign_in.html",contaxt)

def LogOut_View(request):
    logout(request)
    messages.success(request,"You are logged out")
    return redirect("user_auth:user_signin")

@login_required
def User_dashboard(request):
        abstracts=Event_Registration.objects.filter(email=request.user.email)
        f_form=ArticleFilterForm(request.GET)
        if f_form.is_valid():
            status = f_form.cleaned_data['status']
            if status:
                articles = abstracts.filter(status=status)
        user=request.user
        profile=user.profile
        profile=Profile.objects.get(user=request.user)
        if request.method =="POST":
            p_form=ProfileUpdateForm(request.POST,request.FILES ,instance=profile)
            if p_form.is_valid():
                p_form.save()
                
                messages.success(request,"Your information is updated Successfully")
        else:      
            p_form=ProfileUpdateForm(instance=profile)
    
        context={
            'profile':profile,
            'p_form':p_form,
            'f_form':f_form,
            'abstracts':abstracts

        }
        return render(request,"core/user_profile.html",context)


def success(requets):
    return render(requets,'user_auth/success.html')

def token_send(request):
    return render(request,'user_auth/token_send.html')

def verify(request,email_token):
    try:
        user_obj= User.objects.get(email_verification_token=email_token)
        if user_obj:
            user_obj.verified=True
            user_obj.save()
            profile_obj=Profile.objects.create(user=user_obj)
            profile_obj.save()
            messages.success(request,'Congratulations your account is verified')
            return redirect('user_auth:user_signin')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('user_auth:user_signin')

def error_page(request):
    return render(request,'user_auth/error.html')    

def send_email_after_registration(email,email_token,request):
    current_site = get_current_site(request)
    domain = current_site.domain
# Generate the verification URL
    verify_url = reverse('user_auth:verify', kwargs={'email_token': email_token})
    full_verify_url = f'http://{domain}{verify_url}'
    subject='Your account needs to be verify'
    message=f'hi click the link to verify your account: {full_verify_url}'
    
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
