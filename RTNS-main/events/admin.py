from django.contrib import admin
from .models import *
import facebook
# Register your models here.
class SpeechInline(admin.TabularInline):
    model=Speech
    extra=1

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'event_type']
    inlines = [SpeechInline]

    def save_model(self, request, obj, form, change):
        # Save the event model
        super().save_model(request, obj, form, change)

        # Upload event to Facebook
        access_token = "EAAKxkZB0YmZCgBO2ySoQDe1kvHmDrYN4JgTV5shwXMz58spIoX8KmDBJKR621cvgkZCVx8Heyh1cxxtaShZCTfpUcSMW5x91M7P9pCyKjcwLVuWk4l3suM4PHo4PTUigD8ad7QQkbZAHLjsCQOOCZCmsjlAhOKywathDTrxUb3DveJmpLTnyS6PeJROz5g38W5mMsE9ZCbZCxuuMMeS7IGjpeEDygFkFQ7QZD"
        content = f"We are organizing {obj.event_type} event about Recent Trends in Natural Sciences on {obj.date}"
        
        success = self.upload_to_facebook(access_token, content)

        if success:
            self.message_user(request, "Event uploaded to Facebook successfully.")
        else:
            self.message_user(request, "Failed to upload event to Facebook. Please check the logs.")

    def upload_to_facebook(self, access_token, content):
        graph = facebook.GraphAPI(access_token)

        try:
            graph.put_object("me", "feed", message=content)
            return True
        except facebook.GraphAPIError as e:
            print("Facebook API error:", e)
            return False
        
class SpeechAdmin(admin.ModelAdmin):
    list_display=['speech_title','speaker','session_chair','start_time','end_time']


admin.site.register(Event,EventAdmin)
admin.site.register(Speech,SpeechAdmin)




