"""RTNS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from core.views import index
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'user_auth/sign_in.html'  # Adjust the path based on your actual directory structure
    success_url = reverse_lazy('user_dashboard')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("core.urls")),
    path('user/',include("user_auth.urls")),
    path('article/',include("article.urls")),
    path('event/',include("events.urls")),
    path('speakers/',include("speakers.urls")),
    path('contact/',include("contact_us.urls")),
    path('certificate/', include('certificate.urls')),
    path('event_reg/', include('event_reg.urls')),
    path("partial/",include("partials.urls")),
    


    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='user_auth/forget_reset.html'),name='password_reset'),
    path('done/',auth_views.PasswordResetDoneView.as_view(template_name='user_auth/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user_auth/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user_auth/password_reset_complete.html'),name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
