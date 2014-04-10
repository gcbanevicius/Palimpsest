from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import loader, Context, Template

from textview.models import Text

# Create your views here.

#Default view, displays 1 plain text
def index(request, text_name=""):
    temp = loader.get_template('single_text.html')
    gal_war_eng = ""
    c = Context ({
      'text_id': text_name,
      'text1': Text.objects.all(), 
      })

    return HttpResponse(temp.render(c))

#Corresponds to "translate" button, display two texts side by side
def two_text(request, text_name=""):
    temp = loader.get_template('two_text.html')

    c = Context ({
      'text_id': text_name,
      'text_left': Text.objects.all(), 
      'text_right': Text.objects.all()
      })

    return HttpResponse(temp.render(c))


def vocab(request, text_name=""):
    temp = loader.get_template('vocab.html')

    c = Context ({
      'text_id': text_name,
      })

    return HttpResponse(temp.render(c))


