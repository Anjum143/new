from django.contrib import admin
from .models import *
from django.shortcuts import redirect
from django.contrib import messages
# Register your models here.
admin.site.register(SliderImage)
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('admin:partials_websitefooter_changelist')
        super().save_model(request, obj, form, change)
admin.site.register(Patron)

admin.site.register(Gallery)