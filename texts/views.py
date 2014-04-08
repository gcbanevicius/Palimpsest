from django.shortcuts import render
from django.http import HttpResponse

from texts.models import Text

# Create your views here.

def index(request):
    # read the titles from the database
    titles = ""
    for t in Text.objects.all():
        titles += "<a href=%s>%s</a></br>" % (t.title, t.title.replace('_', ' '))
    response_text = titles
    return HttpResponse(response_text)
