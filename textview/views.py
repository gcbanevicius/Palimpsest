from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import loader, Context, Template

from textview.models import Text, QueryForm

from django.views.decorators.csrf import ensure_csrf_cookie

from django.template import RequestContext
#from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

import fake, query, queryEng

# Create your views here.

@ensure_csrf_cookie
def index(request, text_name=""):
    temp = loader.get_template('single_text.html')
    if request.method == 'GET':

        # just get Book 1
        if 'query_range' in request.session:
            q_range = request.session['query_range']
            text = query.startQuery(q_range)
        else:
            text = query.startQuery('1')
            request.session['query_range'] = '1'
          
    elif request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            q_range = str(form.cleaned_data['range'])
            text = query.startQuery(q_range)
            request.session['query_range'] = q_range

    c = RequestContext (request, {
      #'name': 'Caesar',
      'text_id': text_name,
      'gal_war_eng': text, 
     })

    return HttpResponse(temp.render(c))


#Corresponds to "translate" button, display two texts side by side
def two_text(request, text_name=""):
    temp = loader.get_template('two_text.html')

    prev_range = request.session['query_range']
    print 'query_range var:', prev_range

    #c = Context ({
    #  'text_id': text_name,
    #  'text_left': Text.objects.all(), 
    #  'text_right': Text.objects.all()
    #  })

    #return HttpResponse(temp.render(c))
    
    if request.method == 'GET':

        # just get Book 1
        #text_left = query.startQuery('1')
        text_left = query.startQuery(prev_range)
        
        #print text_left[-1][-1]
        text_right = queryEng.startQuery(text_left[0][-1], text_left[-1][-1])

    elif request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            q_range = str(form.cleaned_data['range'])
            request.session['query_range'] = q_range
            text_left = query.startQuery(q_range)
            text_right = queryEng.startQuery(text_left[0][-1], text_left[-1][-1])

    c = RequestContext (request, {
      #'name': 'Caesar',
      'text_id': text_name,
      'text_left': text_left, 
      'text_right': text_right,
     })

    return HttpResponse(temp.render(c))



def vocab(request, text_name=""):
    temp = loader.get_template('vocab.html')

    c = Context ({
      'text_id': text_name,
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
    
 
