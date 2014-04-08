from annoying.decorators import render_to
from django.http import HttpResponse



def home(request):
	temp = loader.get_template('homepage.html')
    return HttpResponse(temp.render())
