from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader, Context, Template

from textview.models import QueryForm, Comment

from django.views.decorators.csrf import ensure_csrf_cookie

from django.template import RequestContext
#from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

import fake, query, queryEng, queryComm

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

    newtext = []
    for i in text:
        newtext.append((i[0], i[2].split()))

    c = RequestContext (request, {
      #'name': 'Caesar',
      'text_id': text_name,
      'text_lines': newtext
     })

    return HttpResponse(temp.render(c))


#Corresponds to "translate" button, display two texts side by side
def two_text(request, text_name=""):
    temp = loader.get_template('two_text.html')

    prev_range = request.session['query_range']

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


    newleft = []
    for i in text_left:
        newleft.append((i[0], i[2].split()))


    c = RequestContext (request, {
      #'name': 'Caesar',
      'text_id': text_name,
      'text_left': newleft, 
      'text_right': text_right,
     })

    return HttpResponse(temp.render(c))

def add_comment(request, text_name=""):
    if request.user.is_authenticated():
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
    else:
        return HttpResponseRedirect('/subscribers/signin')    

def view_comments(request, text_name=""):
    if request.user.is_authenticated():    
        temp = loader.get_template('view_comments.html')

        ###  BEGIN get Latin text  ###
        if 'query_range' in request.session:
            q_range = request.session['query_range']
            text = query.startQuery(q_range)
        else:
            text = query.startQuery('1')
            q_range = '1'
            request.session['query_range'] = q_range
        ###  END get Latin text  ###

        q_range.replace('-', ' ')
        q_list = q_range.split()

        if len(q_list) > -1:
            text_right = queryComm.startQuery(q_range)
        
        elif len(q_list) == 1:
            if '.' in q_list[0]:
            # it's a single line
                text_right =  Comment.objects.filter(path=q_list[0])[0].comment_text
            else:
            # it's a whole book
                start_range = q_list[0]
                end_range = int(q_list[0].split('.')[0]) + 1
                text_lines = Comment.objects.filter(path__gte=start_range).filter(path__lt=end_range)
                
                text_right = []
                for text_line in text_lines:
                    text_right.append( (str(text_line.path), text_line.comment_text) )

        else:
            text_right = ''

        newleft = []
        for i in text:
            newleft.append((i[0], i[2].split()))


        c = RequestContext (request, {
        #'name': 'Caesar',
        'text_id': text_name,
        'text_left': newleft, 
        'text_right': text_right,
        })

        return HttpResponse(temp.render(c))
    else:
        return HttpResponseRedirect('/subscribers/signin')

def vocab(request, text_name=""):
    temp = loader.get_template('vocab.html')

    c = Context ({
      'text_id': text_name,
      })

    return HttpResponse(temp.render(c))
