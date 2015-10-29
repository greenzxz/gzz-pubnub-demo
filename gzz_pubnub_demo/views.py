from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(HttpRequest):
    return HttpResponseRedirect(reverse("chatserver:chat"))