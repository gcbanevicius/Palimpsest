from annoying.decorators import render_to
from django.http import HttpResponse
from django.template import loader, Context, Template



def home(request):
	temp = loader.get_template('homepage.html')
	return HttpResponse(temp.render())
