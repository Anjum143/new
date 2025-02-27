from django.contrib import admin
from contact_us.models import Contact_Us
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','message']
    # search_fields = ['title', 'author__username']
    # list_filter = ['status', 'event']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj) + ('name', 'email', 'subject','message')

        return readonly_fields
# Register your models here.
admin.site.register(Contact_Us,ContactAdmin)