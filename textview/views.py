from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import loader, Context, Template

from textview.models import Text

# Create your views here.

def index(request):
    # attempt at pulling in whole text file from database!
    temp = loader.get_template('single_text.html')
    gal_war_eng = ""
    for t in Text.objects.all():
        gal_war_eng += t.text_field
        gal_war_eng += '\n'
    c = Context ({
      'name': 'Caesar',
      'gal_war_eng': Text.objects.all()
      })
    #return HttpResponse("Hello, world!!! \nIt's me, Palimpsest ;)")
    #arr = gal_war_eng.split('\n')
    #arr_len = len(arr)
    return HttpResponse(temp.render(c))

def two_text(request):
    # attempt at pulling in whole text file from database!
    temp = loader.get_template('two_text.html')
    gal_war_eng = ""
    for t in Text.objects.all():
        gal_war_eng += t.text_field
        gal_war_eng += '\n'
    c = Context ({
      'name': 'Caesar',
      'gal_war_eng': Text.objects.all()
      })
    #return HttpResponse("Hello, world!!! \nIt's me, Palimpsest ;)")
    #arr = gal_war_eng.split('\n')
    #arr_len = len(arr)
    return HttpResponse(temp.render(c))


