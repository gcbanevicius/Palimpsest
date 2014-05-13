from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import loader, Context, Template, RequestContext
from django.contrib.auth.models import User
from textview.models import Comment
from django.core.context_processors import csrf
from textview import views
import urllib2

def index(request):
    temp = loader.get_template('subscribers/index.html')

    c = RequestContext (request, {
      'usersname': User.objects.all()
      })

    return HttpResponse(temp.render(c))

def profile(request, user_name=''):
    temp = loader.get_template('subscribers/profile.html')
    us_er = User.objects.get(username=user_name)


    c = RequestContext (request, {
      'usersname': us_er,
      'user_comments' : Comment.objects.filter(user_id=us_er.id)
      })

    return HttpResponse(temp.render(c))


def signin(request):
    if request.user.is_authenticated():
        return render(request, 'homepage.html')
    else: 
        c = {}
        c.update(csrf(request))    
        request.session['curr_page'] = urllib2.unquote(request.GET.get('next'))
        return render_to_response('subscribers/signin.html', c)

def login_error(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('subscribers/login_error.html', c)
        
def validate(request):
    c = {}
    c.update(csrf(request))   
    if 'q' in request.POST and 'u' in request.POST:
        un = request.POST['q']
        pw = request.POST['u']
        user = authenticate(username=un, password=pw)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                return render_to_response('subscribers/login_error.html', c)
        else:
            return render_to_response('subscribers/login_error.html', c)
    else:
        return render_to_response('subscribers/login_error.html', c)
    #return render(request, 'homepage.html')
    if 'curr_page' in request.session:
        print request.session['curr_page'], "!?!"
        #return render(request, request.session['curr_page'])
        return HttpResponseRedirect(request.session['curr_page'])
    else:
        print 'No session var for last page...'
        return render(request, 'homepage.html')

def signout(request):
    c = {}
    c.update(csrf(request))
    logout(request)
    request.session['curr_page'] = urllib2.unquote(request.GET.get('next'))
    return HttpResponseRedirect(request.session['curr_page'])
    
def signup(request):
    if request.user.is_authenticated():
        return render(request, 'homepage.html')
    else:
        c = RequestContext (request, {
        })
        c.update(csrf(request))
        request.session['curr_page'] = urllib2.unquote(request.GET.get('next'))
        return render_to_response('subscribers/signup.html', c)    

def signup_check(request):
    if 'uname' in request.POST:
        un = request.POST['uname']
        if User.objects.filter(username=un).count():
            c = RequestContext (request, {'sup_error': "Username already in use."
            })
            c.update(csrf(request))
            return render_to_response('subscribers/signup.html', c)  

        else:
            pw = request.POST['pw1']
            pwc = request.POST['pw2']
            em = request.POST['emaila']
            fn = request.POST['firstn']
            ln = request.POST['lastn']
            if pw != pwc: 
                c = RequestContext (request, {'sup_error': "Passwords must match."
                })
                c.update(csrf(request))
                return render_to_response('subscribers/signup.html', c)  
            else:
                User.objects.create_user(un, em, pw, first_name=fn, last_name=ln)
                user = authenticate(username=un, password=pw)
                login(request, user)
                if 'curr_page' in request.session:
                    print request.session['curr_page'], "!?!"
                    #return render(request, request.session['curr_page'])
                    return HttpResponseRedirect(request.session['curr_page'])
                else:
                    print 'No session var for last page...'
                    return render(request, 'homepage.html')
    return render(request, 'homepage.html')
