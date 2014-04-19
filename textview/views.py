from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import loader, Context, Template
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext
from django.core.context_processors import csrf

from textview.models import QueryForm, Comment

import fake, query, queryEng, queryComm

# Create your views here.

#@ensure_csrf_cookie
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
    if request.method == 'GET':
        # just get Book 1
        #text_left = query.startQuery('1')
        text_left = query.startQuery(prev_range)
        
        # now need second to last field, because of comment field
        text_right = queryEng.startQuery(text_left[0][-2], text_left[-1][-2])

    elif request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            q_range = str(form.cleaned_data['range'])
            request.session['query_range'] = q_range
            text_left = query.startQuery(q_range)
            text_right = queryEng.startQuery(text_left[0][-2], text_left[-1][-2])
        else:
            if 'query_range' in request.session:   
                q_range = '1'
            request.session['query_range'] = q_range
            text_left = query.startQuery(q_range)
            text_right = queryEng.startQuery(text_left[0][-2], text_left[-1][-2])

    c = RequestContext (request, {
      #'name': 'Caesar',
      'text_id': text_name,
      'text_left': text_left, 
      'text_right': text_right,
     })

    return HttpResponse(temp.render(c))

def add_comment(request, text_name=""):
    temp = loader.get_template('single_text.html')

    if request.is_ajax():
        comment = Comment(path=request.POST['line'], user_id='1', text_name=request.POST['text_name'], comment_text=request.POST['comment_text'])
        query.insertComment(request.POST['line'], request.POST['comment_text'])

    c = RequestContext(request, {
      'text_id': text_name,
      'text_left': '',#Text.objects.all(), 
      'text_right': '',#Text.objects.all()
      })

    return HttpResponse(temp.render(c))

def view_comments(request, text_name=""):
    temp = loader.get_template('view_comments.html')

    ###  BEGIN get Latin text  ###
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            q_range = str(form.cleaned_data['range'])
            request.session['query_range'] = q_range
        else:
            if 'query_range' in request.session:   
                q_range = request.session['query_range'] 
            else:
                q_range = '1'
                request.session['query_range'] = q_range

    elif request.method == 'GET':
        if 'query_range' in request.session:
            q_range = request.session['query_range']
        else:
            q_range = '1'
            request.session['query_range'] = q_range
    
    text_left = query.startQuery(q_range)
    ###  END get Latin text  ###

    #print text_left, "-.-.-"

    q_range.replace('-', ' ')
    q_list = q_range.split()

    text_right = queryComm.startQuery(q_range)
    
    c = RequestContext(request, {
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
