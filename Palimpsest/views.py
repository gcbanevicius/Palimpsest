from annoying.decorators import render_to
from django.http import HttpResponse

#@render_to 'navbar.html'
#def home
#    return

def hello_world(request):
    return HttpResponse("Hello, World")
