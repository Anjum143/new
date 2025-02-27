from django.contrib import admin
from contact_us.models import Contact_Us
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','message']
    readonly_fields =['name', 'email', 'subject','message']
    def has_add_permission(self, request):
        return False
    
# Register your models here.
admin.site.register(Contact_Us,ContactAdmin)