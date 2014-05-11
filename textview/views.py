from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader, Context, Template
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext
from django.core.context_processors import csrf

from textview.models import QueryForm, Comment
from django.contrib.auth.models import User
import query
import queryEng
import queryComm

# Create your views here.

def render_error(request, error_msg, text_name = ''):
    temp = loader.get_template('error.html')
   
    text = [error_msg] + [
        ('', '', 'Enter a query range at left in one of the following forms (hypen optional):', '', ''),
        ('', '', 'Line to line (e.g. 1.10-2.10)', '', ''),
        ('', '', 'Book to book (e.g. 1-2)', '', ''),
        ('', '', 'A single line (e.g. 1.10)', '', ''),
        ('', '', 'A single book (e.g. 1)', '', ''),        
    ]

    print text

    c = RequestContext (request, {
        'text_id': text_name,
        'text_lines': text,
    })

    return HttpResponse(temp.render(c))

def index(request, text_name=""):
    temp = loader.get_template('single_text.html')

    if request.method == 'GET':
        # if we already asked for a range
        if 'query_range' in request.session:
            q_range = request.session['query_range']
            text = query.startQuery(q_range)
            error = text[1] # error from query.py
            text = text[0] # actual list of text-tuples
            if error != 0:
                return render_error(request, text[0], text_name)
        # else give a welcome message
        else:
            return render_error(request, ('', '', 'Welcome to Palimpsest!', '', ''), text_name)

    elif request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():            
            q_range = str(form.cleaned_data['range'])
            text = query.startQuery(q_range)
            error = text[1] # error from query.py
            text = text[0] # actual list of text-tuples
            if error != 0:
                return render_error(request, text[0], text_name)
            # set the query_range session variable 
            request.session['query_range'] = q_range
        # if it was an invalid form, print suggestion message
        else:
            return render_error(request, ('', '', '', '', ''), text_name)

    newtext = []
    #print text
    for i in text:
        newtext.append((i[0], i[2].split()))

    c = RequestContext (request, {
      'text_id': text_name,
      'text_lines': newtext,
      #'error_mode': request.session['error_mode'] # pass in "error_mode", so we can choose correct layout
     })

    #print text
    return HttpResponse(temp.render(c))


#Corresponds to "translate" button, display two texts side by side
def two_text(request, text_name=""):
    temp = loader.get_template('two_text.html')

    if request.method == 'GET':
        # if we already asked for a range
        if 'query_range' in request.session:
            q_range = request.session['query_range']
            text_left = query.startQuery(q_range)
            error = text_left[1] # error from query.py
            text_left = text_left[0] # actual list of text-tuples
            if error != 0:
                return render_error(request, text_left[0], text_name)
        # else give a welcome message
        else:
            return render_error(request, ('', '', 'Welcome to Palimpsest!', '', ''), text_name)

        # now need second to last field, because of comment field
        print text_left[0], text_left[-1]
        text_right = queryEng.startQuery(text_left[0][-2], text_left[-1][-2])

    elif request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            q_range = str(form.cleaned_data['range'])
            request.session['query_range'] = q_range
            text_left = query.startQuery(q_range)
            error = text_left[1] # error from query.py
            text_left = text_left[0] # actual list of text-tuples
           
            # if error mode engaged, go no further
            if error != 0: 
                return render_error(request, text_left[0], text_name) 

            print text_left[0], text_left[-1]
            text_right = queryEng.startQuery(text_left[0][-2], text_left[-1][-2])

        # if it was an invalid form, print suggestion message
        else:
            return render_error(request, ('', '', '', '', ''), text_name)

    newleft = []
    for i in text_left:
        newleft.append((i[0], i[2].split()))

    c = RequestContext (request, {
      'text_id': text_name,
      'text_left': newleft, 
      'text_right': text_right,
     })

    return HttpResponse(temp.render(c))

# called from chagneMethod in base.html
# checks to see if user is authenticated,
# if not, redirect to signin page 
def auth_user(request):

    return 1

def add_comment(request, text_name=""):
    if request.user.is_authenticated():
        temp = loader.get_template('add_comment.html')

        if request.is_ajax():
            path = request.POST['line']
            path = path.split('.')
            
            # NB POST['is_pub'] must be '1' for TRUE, '0' f`r FALSE
            if request.POST['is_pub'] == '1':
                # if error mode engaged, go no further
                #print "id = 0, public = t"
                comment = Comment(book=int(path[0]), line=int(path[1]), user_id=request.user.id, public=1, text_name=request.POST['text_name'], comment_text=request.POST['comment_text'])
            elif request.POST['is_pub'] == '2':
                comment = Comment(book=int(path[0]), line=int(path[1]), user_id=0, public=1, text_name=request.POST['text_name'], comment_text=request.POST['comment_text'])
            else:
                comment = Comment(book=int(path[0]), line=int(path[1]), user_id=request.user.id, public=0, text_name=request.POST['text_name'], comment_text=request.POST['comment_text'])

            comment.save()
            #query.insertComment(request.POST['line'], request.POST['comment_text'])

        # this else is a dummy clause, remove later
        else:
            print "Not AJAX, I suppose..."

        c = RequestContext(request, {
          'text_id': text_name,
          'text_left': '',#Text.objects.all(), 
          'text_right': '',#Text.objects.all()
          })
        
        #print "print the user id!"
        #print request.user.id
        #print request.POST['is_pub']

        return HttpResponse(temp.render(c))

    else:
    #    print '/subscribers/signin?next=%s' % request.get_full_path() 
        return HttpResponseRedirect('/subscribers/signin') #?next=%s' % request.get_full_path() )    

def view_comments(request, text_name=""):
    if request.user.is_authenticated():    
        temp = loader.get_template('view_comments.html')

        ###  BEGIN get Latin text  ###
        if request.method == 'POST':
            # set 'comment_type', since we know it's a POST
            if 'comment_type' in request.POST:
                #print request.POST['comment_type'], 'hiya'
                request.session['comment_view_mode'] = request.POST['comment_type']

            form = QueryForm(request.POST)
            if form.is_valid():
                q_range = str(form.cleaned_data['range'])
                request.session['query_range'] = q_range
            # if form was invalid, return suggestion message
            else:
                return render_error(request, ('', '', '', '', ''), text_name)

        elif request.method == 'GET':
            if 'query_range' in request.session:
                q_range = request.session['query_range']
            # if we haven't made a previous query, return suggestion message
            else:
                return render_error(request, ('', '', '', '', ''), text_name)
    
        text_left = query.startQuery(q_range)
        error = text_left[1] # error from query.py
        text_left = text_left[0] # actual list of text-tuples

        if error != 0:
            return render_error(request, text_left[0], text_name)
 
        #print text_left
    ###  END get Latin text  ###

        # set view mode based on pre-stored var; else PUBLIC (1)
        if 'comment_view_mode' in request.session:
            view_mode = request.session['comment_view_mode']
        else:
            view_mode = 1

        q_range.replace('-', ' ')
        q_list = q_range.split()

        text_right = queryComm.startQuery(q_range, int(view_mode), request.user.id) # I am SICK of everything being a string...

        newleft = []
        for i in text_left:
            newleft.append((i[0], i[2].split(), i[3]))

        c = RequestContext (request, {
            'text_id': text_name,
            'text_left': newleft, 
            'text_right': text_right,
            'user_names': User.objects.all()
        })

        return HttpResponse(temp.render(c))
        
    else:
        request.session['curr_page'] = request.get_full_path()
        return HttpResponseRedirect('/subscribers/signin')

def vocab(request, text_name=""):
    temp = loader.get_template('vocab.html')

    c = Context ({
      'text_id': text_name,
      })

    return HttpResponse(temp.render(c))
    
    
def view_critical(request, text_name="", isbn_num='ISBN:1909254150'):
    if request.user.is_authenticated():    
        temp = loader.get_template('view_critical.html')

        ###  BEGIN get Latin text  ###
        if request.method == 'POST':
            print 'Post it!'
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
            print 'Get it!'
            if 'query_range' in request.session:
                q_range = request.session['query_range']
            else:
                q_range = '1'
                request.session['query_range'] = q_range
    
        text_left = query.startQuery(q_range)
        error = text_left[1] # error from query.py
        text_left = text_left[0] # actual list of text-tuples
 
    ###  END get Latin text  ###

        newleft = []
        for i in text_left:
            newleft.append((i[0], i[2].split()))

        c = RequestContext (request, {
            'text_id': text_name,
            'text_left': newleft,
            'isbn': isbn_num, 
        })

        return HttpResponse(temp.render(c))
    else:
        return HttpResponseRedirect('/subscribers/signin')


