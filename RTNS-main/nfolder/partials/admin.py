from django.contrib import admin
from .models import *
# Register your models here.
class DepartmentLogoInline(admin.TabularInline):
    model = DepartmentLogo
    extra = 1

class HeaderAdmin(admin.ModelAdmin):
    inlines = [DepartmentLogoInline]
    
    
    
    def save_model(self, request, obj, form, change):
        obj.save()  # Save the Header instance first
        super().save_model(request, obj, form, change) 

admin.site.register(WebsiteHeader, HeaderAdmin)

class FooterAdmin(admin.ModelAdmin):
    list_display=['title']
admin.site.register(WebsiteFooter,FooterAdmin)  



