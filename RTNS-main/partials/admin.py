from django.contrib import admin
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
# Register your models here.
class DepartmentLogoInline(admin.TabularInline):
    model = DepartmentLogo
    extra = 1

@admin.register(WebsiteHeader)
class WebsiteHeaderAdmin(admin.ModelAdmin):
    inlines = [DepartmentLogoInline]

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('admin:partials_websiteheader_changelist')
        super().save_model(request, obj, form, change)




@admin.register(WebsiteFooter)
class WebsiteFooterAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('admin:partials_websitefooter_changelist')
        super().save_model(request, obj, form, change)
admin.site.register(SponsorLogo) 



