from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(HttpRequest):
    return HttpResponse("Server is up!")