from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

import json

from .models import Channel

from pubnub_conn import myPubnubConn


# Create your views here.

def index(request):
    channels = Channel.objects.all()
    return HttpResponse("There are %d channels active." % (len(channels),))

def create(request):
    try:
        channel_text=str(request.POST['name'])
    except (KeyError):
        channel_text="a-default-channel"

    try:
        channel = Channel.objects.get(pk=channel_text)
    except (KeyError, Channel.DoesNotExist):
        Channel(channel_name=channel_text).save()

    return HttpResponseRedirect(reverse('chatserver:index'))

def sent(request):
    return HttpResponse("Message sent.")

@csrf_exempt
def login_user(request):
    """
    Logins a user by confirming the user exists and returns the subscription key so they can be on the same network
    :param request:
    :return:
    """
    #user = authenticate(username=request.POST['username'], password=request.POST['password'])
    #login(request, user)
    return HttpResponse(json.dumps({'sub_key': myPubnubConn.subscribe_key, 'channel': myPubnubConn.default_channel}))


@csrf_exempt
def send(request):
    # Future development: use shared sessions to store this connection rather than recreate one each time
    conn = myPubnubConn.MyPubnubConn()
    try:
        message_text = str(request.POST['text'])
        message_source = str(request.POST['source'])
        conn.publish({'msg': message_text, 'source': message_source})
    except (KeyError):
        message_text = "Channel is ready for notifications."
        conn.publish(message_text)

    return HttpResponseRedirect(reverse('chatserver:sent'))