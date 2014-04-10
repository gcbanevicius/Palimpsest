from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import loader, Context, Template

from textview.models import Text

# Create your views here.

def index(request, text_name=""):
    # attempt at pulling in whole text file from database!
    temp = loader.get_template('single_text.html')
    gal_war_eng = ""
    c = Context ({
      'gal_war_eng': Text.objects.all(), 
      })

    return HttpResponse(temp.render(c))

def two_text(request, text_name=""):
    # attempt at pulling in whole text file from database!
    temp = loader.get_template('two_text.html')

    gal_war_eng = ""

    c = Context ({
      'test':text_name,
      'gal_war_eng': Text.objects.all(), 
      })

    return HttpResponse(temp.render(c))


