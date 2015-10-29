from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie

import json

from .models import Channel

from pubnub_conn import myPubnubConn

# Create your views here.
title = "Green's Simple Chatty"

@ensure_csrf_cookie
def chat(request):
    """
    Primary HTML page that does the chatting.
    :param request:
    :return:
    """
    context = RequestContext(request, {
        'title' : title,
    })
    return render(request, 'chatserver/chat.html', context=context)

def sent(request):
    """
    Empty page meant to assert that a message has been published.  Does not guarantee a successful message though.
    :param request:
    :return:
    """
    return HttpResponse("Message sent.")

@ensure_csrf_cookie
def get_user_keys(request):
    """
    Logins a user by confirming the user exists and returns the subscription key so they can be on the same network
    :param request:
    :return:
    """
    pubnub_details = {
        'subscribe_key': myPubnubConn.subscribe_key,
        'publish_key': myPubnubConn.publish_key,
        'channel': myPubnubConn.default_channel,
    }
    #user = authenticate(username=request.POST['username'], password=request.POST['password'])
    #login(request, user)
    return render(request, 'chatserver/sub_authorized.template', pubnub_details)

def send(request):
    # Future development: use shared sessions to store this connection rather than recreate one each time

    try:
        channel = request.POST['channel']
        message_text = request.POST['text']
        message_source = request.POST['user']
        message_type = 'text'
    except (KeyError):
        channel=myPubnubConn.default_channel
        message_text = "Did not receive message from user."
        message_source = "Chat server"
        message_type = 'alert'

    conn = myPubnubConn.MyPubnubConn(channel=channel)
    conn.publish({'text': message_text, 'user': message_source, 'msg_type' : message_type})
    return HttpResponseRedirect(reverse('chatserver:sent'))