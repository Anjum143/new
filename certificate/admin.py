from django.contrib import admin
from django.urls import reverse,path

from .models import *
from .views import *



from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import *
from .views import *

class CertificateAdmin(admin.ModelAdmin):
    change_list_template = 'admin/certificate/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create-certificate/', self.admin_site.admin_view(create), name='create_certificate'),
            path('show-status/', self.admin_site.admin_view(view_certificate_status), name='show_status'),
        ]
        return custom_urls + urls

    def get_model_perms(self, request):
        return {}

    def add_certificate_button(self, obj=None):
        url = reverse('admin:create_certificate')
        return format_html('<a class="button" href="{}">Add Certificate</a>', url)
    add_certificate_button.short_description = 'Add Certificate'

    def show_status_button(self, obj=None):
        url = reverse('admin:show_status')
        return format_html('<a class="button" href="{}">Show Status</a>', url)
    show_status_button.short_description = 'Show Status'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_certificate_button'] = self.add_certificate_button()
        extra_context['show_status_button'] = self.show_status_button()
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Event, CertificateAdmin)