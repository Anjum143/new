from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.core.mail import send_mail
# Register your models here.
from django.contrib import admin

from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from .models import *
from .utils import retrieve_file_content
from django.conf import settings


class SubAreaInline(admin.TabularInline):
    model=SubArea
    extra=1
class AreaAdmin(admin.ModelAdmin):
    inlines=[SubAreaInline]

admin.site.register(Area,AreaAdmin)

@admin.register(Event_Registration)
class RegAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'file_id', 'area','status','abstract_category']
    change_form_template = 'admin/event_reg/registration_change_form.html'
    
    def has_add_permission(self, request):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        all_fields = [field.name for field in self.model._meta.get_fields()]
        excluded_fields = ['status','reason']
        readonly_fields = list(set(all_fields) - set(excluded_fields))
        return readonly_fields
    
    def get_changeform_initial_data(self, request):
        obj = self.get_object(request, request.resolver_match.args, '')
        if obj and obj.reg_purpose != 'abstract':
            self.change_form_template = 'admin/change_form.html'
        return super().get_changeform_initial_data(request)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        extra_context['file_content'] = retrieve_file_content(obj.file_id)
        extra_context['status'] = obj.status
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
    def save_model(self, request, obj, form, change):
        obj.save()
        if change and 'status' in form.changed_data:
            
            new_status = form.cleaned_data['status']
            reason = form.cleaned_data['reason']
            if new_status == 'approveforposter':
                subject = 'Your request has been approved'
                message = f'Your request has been approved for poster. Reason: {reason}'
            elif new_status == 'rejected':
                subject = 'Your request has been rejected'
                message = f'Your request has been rejected. Reason: {reason}'
            elif new_status == 'pending':
                subject = 'Your request is pending'
                message = f'Your request is currently pending for review. Reason: {reason}'
            elif new_status == 'approveforpresentation':
                subject = 'Your request is approved'
                message = f'Your request is approved  for presentation. Reason: {reason}'

            user_email = obj.email 
            send_mail(subject, message,settings.EMAIL_HOST_USER , [user_email])
            










    
    
