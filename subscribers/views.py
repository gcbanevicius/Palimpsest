from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import loader, Context, Template
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from textview import views
import urllib2

def index(request):
    temp = loader.get_template('subscribers/index.html')

    c = Context ({
      'usersname': User.objects.all()
      })

    return HttpResponse(temp.render(c))

def profile(request, user_name=''):
    temp = loader.get_template('subscribers/profile.html')

    c = Context ({
      'usersname': User.objects.get(username=user_name)
      })

    return HttpResponse(temp.render(c))


def signin(request):
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
    c = {}
    c.update(csrf(request))
    return render_to_response('subscribers/signup.html', c)    

def signup_success(request):
    if 'uname' in request.POST:
        un = request.POST['uname']
        if User.objects.filter(username=un).count():
            return render(request, 'subscribers/signup.html')

        else:
            pw = request.POST['pw1']
            pwc = request.POST['pw2']
            em = request.POST['emaila']
            fn = request.POST['firstn']
            ln = request.POST['lastn']
        
            User.objects.create_user(un, em, pw, first_name=fn, last_name=ln)

            if 'curr_page' in request.session:
                print request.session['curr_page'], "!?!"
                return render(request, request.session['curr_page'])
            else:
                print 'No session var for last page...'
                return render(request, 'homepage.html')
