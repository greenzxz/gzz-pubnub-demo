from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Channel

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