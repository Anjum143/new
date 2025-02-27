from django.contrib import admin
from .models import *
from django.http import HttpResponse
import csv

class BaseSpeakersAdmin(admin.ModelAdmin):
    list_display = ['name','email', 'designation','speaker_type']

    def generate_speakers_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="speakers.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Image', 'Designation', 'Speaker Type','Email'])
        image_url=''
        for speaker in queryset:
            writer.writerow([speaker.name, image_url, speaker.designation, speaker.speaker_type,speaker.email])

        return response

    generate_speakers_csv.short_description = 'Generate CSV for selected speakers'


class SpeakerAdmin(BaseSpeakersAdmin):
    list_display=['name','email','designation']
    actions=['generate_speakers_csv']
    def generate_speakers_csv(self, request, queryset):
        return super().generate_speakers_csv(request, queryset)
admin.site.register(Speaker,SpeakerAdmin)  

