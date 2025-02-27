from django.shortcuts import render,get_object_or_404,redirect
from .models import Event,Speech,LiveStream, Message
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError, JsonResponse
from user_auth.models import User
from django.core import serializers
from .forms import EventRegistrationForm
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def Events(request):

    events=Event.objects.all()
    speechs=Speech.objects.all() 
    context={
        'events':events,
        'speechs':speechs,
    }
    return render(request,"core/event.html",context)



def live_stream(request, event_id):
    try:
        # Retrieve the Event object
        event = get_object_or_404(Event, id=event_id)

        # Retrieve the LiveStream object associated with the Event
        live_stream = get_object_or_404(LiveStream, event=event)

        # Retrieve all messages associated with the LiveStream
        messages = Message.objects.filter(live_stream=live_stream)

        context = {
            'event': event,
            'live_stream': live_stream,
            'messages': messages,
        }

        return render(request, 'core/live_stream.html', context)

    except Event.DoesNotExist:
        return HttpResponseServerError("Event does not exist.")

    except LiveStream.DoesNotExist:
        return HttpResponseServerError("Live stream does not exist.")

def post_message(request, event_id):
    try:
        if request.method == 'POST':
            # Retrieve the LiveStream object associated with the Event
            live_stream = get_object_or_404(LiveStream, event_id=event_id)
            user=request.user
            
    # }
            print("he",user)
            # Retrieve the message text from the request
            message_text = request.POST.get('message')
            print("hello",message_text)
            # Create a new Message object
            message = Message.objects.create(live_stream=live_stream, text=message_text,user=user)
            serialized_user = serializers.serialize('json', [user])
            user_data = serialized_user[1:-1]
            response_data = {
                'success': True,
                'message': {
                    'text': message.text,
                    'timestamp': message.timestamp,
                    'user':user_data
                }
            }
            
            # Return a JSON response indicating success
            return JsonResponse(response_data)

    except LiveStream.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Live stream does not exist.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def event_registration(request):
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Add any additional logic or redirect to a success page
    else:
        form = EventRegistrationForm()

    return render(request, 'core/event_registration.html', {'form': form})


