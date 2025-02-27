from django.shortcuts import render,redirect
from user_auth.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.contrib import messages
from django.contrib.messages import constants
from django.conf import settings
from user_auth.models import Profile,User
from article.models import Article
from article.forms import ArticleFilterForm
from .forms import ProfileUpdateForm,UserUpdateForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.hashers import make_password


# Create your views here.
def sign_up(requst):
    # form = UserRegisterForm(requst.POST or None)
    password_warnings=["Atleast 8 characters.",
                       "Not include username.",
                       "Don't use common password."]
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
            username=form.cleaned_data.get("username")
            # messages.success(requst,f"Hey {username} your account has been created")
            # new_user=authenticate(username=form.cleaned_data['email'],
            #                       password=form.cleaned_data['password1'])
            
            # login(requst,new_user)
            return redirect("user_auth:user_dashboard")
    else:
        form=UserRegisterForm()      
    context={
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
    contaxt={
        'is_sign_in_page' :is_sign_in_page
    }   

    return render(request,"user_auth/sign_in.html",contaxt)

def LogOut_View(request):
    logout(request)
    messages.success(request,"You are logged out")
    return redirect("user_auth:user_signin")

@login_required
def User_dashboard(request):
    
        articles=Article.objects.filter(author=request.user)
        f_form=ArticleFilterForm(request.GET)
        if f_form.is_valid():
            status = f_form.cleaned_data['status']
            if status:
                articles = articles.filter(status=status)
            # if request.is_ajax():
            #     return render_to_response('partial_article_list.html', {'articles': articles})

        user=request.user
        profile=user.profile
        profile=Profile.objects.get(user=request.user)
        print(user)
        if request.method =="POST":
            p_form=ProfileUpdateForm(request.POST,request.FILES ,instance=profile)
            u_form=UserUpdateForm(request.POST,instance=user)
            if p_form.is_valid() and u_form.is_valid():
                p_form.save()
                u_form.save()
                messages.success(request,"Your information is updated Successfully")
        else:      
            p_form=ProfileUpdateForm(instance=profile)
            u_form=UserUpdateForm(instance=user)
    
        context={
            'profile':profile,
            'p_form':p_form,
            'u_form':u_form,
            'articles':articles,
            'f_form':f_form,

        }
        return render(request,"core/user_profile.html",context)


def success(requets):
    return render(requets,'user_auth/success.html')

def token_send(request):
    return render(request,'user_auth/token_send.html')

def verify(request,email_token):
    try:
        user_obj= User.objects.get(email_verification_token=email_token)
        print("hello",user_obj.email_verification_token)
        print("asdf",user_obj)
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
    print("1")
    domain = current_site.domain
    print("2")
# Generate the verification URL
    verify_url = reverse('user_auth:verify', kwargs={'email_token': email_token})
    print("3")
    full_verify_url = f'http://{domain}{verify_url}'
    print("4")
    subject='Your account needs to be verify'
    message=f'hi click the link to verify your account: {full_verify_url}'
    # http://127.0.0.1:8000/user/verify/{email_token}'
    
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
