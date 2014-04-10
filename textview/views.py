from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import loader, Context, Template

from textview.models import Text, QueryForm

from django.views.decorators.csrf import ensure_csrf_cookie

from django.template import RequestContext
#from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

import fake, query

# Create your views here.

#@csrf_exempt
@ensure_csrf_cookie
def index(request):
    temp = loader.get_template('single_text.html')
    if request.method == 'GET':

        # just get Book 1
        text = query.startQuery('1')

    elif request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            text = query.startQuery(str(form.cleaned_data['range']))

    c = RequestContext (request, {
      'name': 'Caesar',
      'gal_war_eng': text, 
      })

    return HttpResponse(temp.render(c))


#@csrf_exempt
@ensure_csrf_cookie
def two_text(request):
    # attempt at pulling in whole text file from database!
    temp = loader.get_template('two_text.html')
    
    #gal_war_eng = ""
    #for t in Text.objects.all():
    #    gal_war_eng += t.text_field
    #    gal_war_eng += '\n'
    
    # abridged way (just get one line)
    #t = Text.objects.first()
    #gal_war_eng = t.text_field + '\n'

    #fake.main() 

    text = Text.objects.first()

    form = QueryForm(request.POST)
    if request.method == 'POST':
        print 'Data is:', form.data
        if form.is_valid():
            print 'Range is:', form.cleaned_data['range']
            text = query.startQuery(str(form.cleaned_data['range']))
        else:
            print 'Nope'

    print "Text is:", text

    c = RequestContext (request, {
      'name': 'Caesar',
      'gal_war_eng': text, #Text.objects.first() #.all()
      })

    return HttpResponse(temp.render(c))




############ OLD CODE ###############
    #gal_war_eng = ""
    #for t in Text.objects.all():
    #    gal_war_eng += t.text_field
    #    gal_war_eng += '\n'
    
    # abridged way (just get one line)
    #t = Text.objects.first()
    #gal_war_eng = t.text_field + '\n'
    
 
